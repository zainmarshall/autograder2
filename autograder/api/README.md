# API Folder Structure and Documentation

This folder contains the new django api thingies. So like if you want to see the api iteself go to localhost:3000/swagger/ and you can see and test the endpoints. The files themselves include the um like api returns.

Please don't look at git blame for who wrote the docs.
## File Overview

- **serializers.py**: Creates objects for the thingies and then returns them. 
- **problem_list_api.py**: Contains `ProblemListAPI`, which provides the `/api/problems/` endpoint (GET: list all problems).
- **problem_detail_api.py**: Contains `ProblemDetailAPI`, which serializers.py: DRF serializers for Problems and Rankings. Handles data validation and transformation for API responses.
provides the `/api/problems/<pid>/` endpoint (GET: fetch a single problem by ID).
- **rankings_api.py**: Contains `RankingsAPI`, which provides the `/api/rankings/<season>/` endpoint (GET: fetch rankings for a season).
- **contest_serializers.py**: DRF serializer for Contest objects.
- **contest_views.py**: Contains `ContestListAPI` and `ContestDetailAPI` for `/api/contests/` and `/api/contests/<cid>/` endpoints.
- **urls.py**: Collects and exposes all API endpoints under the `/api/` prefix for the Django project.

## Adding New Endpoints
- Create a new file for each new resource or endpoint (e.g., `submission_list_api.py`).
- Define your APIView class in that file.
- Add the endpoint to `urls.py` by importing your class and adding a `path()` entry.

## Example Endpoints
- `GET /api/problems/` — List all problems
- `GET /api/problems/<pid>/` — Get details for a specific problem
- `GET /api/rankings/<season>/` — Get rankings for a season
- `GET /api/contests/` — List all contests
- `GET /api/contests/<cid>/` — Get details for a specific contest

## Notes
- All new API code should go in this folder, not in the legacy app folders.
- Use clear, descriptive filenames for each endpoint or resource.
- Use DRF class-based views and serializers for all new APIs.
