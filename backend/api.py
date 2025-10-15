"""
FastAPI backend for Speaker Prospect Filtering Tool.
Handles CSV upload and speaker filtering with NaN-safe processing.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sys
import os
from datetime import datetime
import json
import pandas as pd
import io

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from filters import SpeakerFilter
from output_generator import OutputGenerator

app = FastAPI(
    title="Speaker Prospect Filtering API",
    description="API for filtering and organizing speaker prospects from CSV files",
    version="2.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Increase max request size to 1GB
app.max_request_size = 1024 * 1024 * 1024  # 1GB


class FilterRequest(BaseModel):
    """Request model for filtering speakers (legacy - use file upload instead)."""
    event_name: str
    event_title: Optional[str] = ""
    csv_data: Optional[str] = None  # Base64 encoded CSV data


class FilterResponse(BaseModel):
    """Response model for filtered speakers."""
    event_name: str
    event_title: str
    generated_at: str
    summary: dict
    confirmed_speakers: List[dict]
    intended_speakers: List[dict]
    endorsed_speakers: List[dict]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str


class CSVInfoResponse(BaseModel):
    """CSV file information response."""
    row_count: int
    column_count: int
    columns: List[str]
    sample_data: List[dict]
    message: str


@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Speaker Prospect Filtering API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "test_connection": "/api/test-connection",
            "filter_speakers": "/api/filter-speakers",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/upload-csv", response_model=CSVInfoResponse)
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload CSV file and return basic information about it.
    Max file size: 1GB
    """
    try:
        # Check file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=400,
                detail="File must be a CSV file"
            )
        
        # Read CSV file
        contents = await file.read()
        
        # Check file size (1GB limit)
        if len(contents) > 1024 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="File size exceeds 1GB limit"
            )
        
        # Parse CSV
        df = pd.read_csv(io.BytesIO(contents))
        
        # Get sample data (first 3 rows)
        sample_data = df.head(3).to_dict('records')
        
        return {
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": df.columns.tolist(),
            "sample_data": sample_data,
            "message": f"Successfully uploaded. Found {len(df)} rows and {len(df.columns)} columns."
        }
    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=400,
            detail="CSV file is empty"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing CSV: {str(e)}"
        )


@app.post("/api/filter-speakers-csv")
async def filter_speakers_from_csv(
    event_name: str,
    event_title: str = "",
    file: UploadFile = File(...)
):
    """
    Filter speakers from uploaded CSV file based on event name.
    
    Args:
        event_name: Name of the event (e.g., "2511 Barclays")
        event_title: Optional event title for content analysis
        file: CSV file with speaker data
        
    Returns:
        FilterResponse with categorized speakers
    """
    try:
        # Read and parse CSV
        contents = await file.read()
        
        # Check file size
        if len(contents) > 1024 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="File size exceeds 1GB limit"
            )
        
        df = pd.read_csv(io.BytesIO(contents))
        records = df.to_dict('records')
        
        if not records:
            raise HTTPException(
                status_code=404,
                detail="No records found in CSV file"
            )
        
        # Filter speakers into categories
        speaker_filter = SpeakerFilter(event_name)
        
        confirmed = speaker_filter.filter_confirmed(records)
        intended = speaker_filter.filter_intended(records)
        endorsed = speaker_filter.filter_endorsed(records)
        
        # Generate enhanced data with analysis
        generator = OutputGenerator(event_name, event_title)
        
        # Enhance intended and endorsed speakers with analysis
        enhanced_intended = [generator._enhance_speaker_data(s) for s in intended]
        enhanced_endorsed = [generator._enhance_speaker_data(s) for s in endorsed]
        
        return {
            "event_name": event_name,
            "event_title": event_title,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "confirmed_count": len(confirmed),
                "intended_count": len(intended),
                "endorsed_count": len(endorsed),
                "total_count": len(confirmed) + len(intended) + len(endorsed)
            },
            "confirmed_speakers": confirmed,
            "intended_speakers": enhanced_intended,
            "endorsed_speakers": enhanced_endorsed
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error filtering speakers: {str(e)}"
        )


@app.post("/api/export-csv/{format}")
async def export_speakers_from_csv(
    format: str,
    event_name: str,
    event_title: str = "",
    file: UploadFile = File(...)
):
    """
    Export filtered speakers from CSV in specified format (csv, json, text).
    
    Args:
        format: Export format (csv, json, text)
        event_name: Name of the event
        event_title: Optional event title
        file: CSV file with speaker data
        
    Returns:
        File download response
    """
    from fastapi.responses import Response
    
    if format not in ['csv', 'json', 'text']:
        raise HTTPException(
            status_code=400,
            detail="Invalid format. Must be csv, json, or text"
        )
    
    try:
        # Read and parse CSV
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        records = df.to_dict('records')
        
        # Filter speakers
        speaker_filter = SpeakerFilter(event_name)
        confirmed = speaker_filter.filter_confirmed(records)
        intended = speaker_filter.filter_intended(records)
        endorsed = speaker_filter.filter_endorsed(records)
        
        generator = OutputGenerator(event_name, event_title)
        
        # Generate appropriate format
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"speaker_report_{timestamp}"
        
        if format == 'csv':
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
                generator.generate_csv(confirmed, intended, endorsed, f.name)
                with open(f.name, 'r', encoding='utf-8') as csv_file:
                    content = csv_file.read()
                os.unlink(f.name)
            
            return Response(
                content=content,
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename={filename}.csv"
                }
            )
            
        elif format == 'json':
            data = {
                'event_name': event_name,
                'event_title': event_title,
                'generated_at': datetime.now().isoformat(),
                'summary': {
                    'confirmed_count': len(confirmed),
                    'intended_count': len(intended),
                    'endorsed_count': len(endorsed)
                },
                'confirmed_speakers': confirmed,
                'intended_speakers': [generator._enhance_speaker_data(s) for s in intended],
                'endorsed_speakers': [generator._enhance_speaker_data(s) for s in endorsed]
            }
            
            return Response(
                content=json.dumps(data, indent=2, ensure_ascii=False),
                media_type="application/json",
                headers={
                    "Content-Disposition": f"attachment; filename={filename}.json"
                }
            )
            
        else:  # text
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                generator.generate_text(confirmed, intended, endorsed, f.name)
                with open(f.name, 'r', encoding='utf-8') as text_file:
                    content = text_file.read()
                os.unlink(f.name)
            
            return Response(
                content=content,
                media_type="text/plain",
                headers={
                    "Content-Disposition": f"attachment; filename={filename}.txt"
                }
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error exporting data: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



