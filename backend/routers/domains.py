from fastapi import APIRouter, Request
router = APIRouter()

@router.get("")
async def list_domains(request: Request):
    return {"domains": request.app.state.kb.domains}

@router.get("/phases")
async def list_phases(request: Request):
    return {"phases": request.app.state.kb.phases}
