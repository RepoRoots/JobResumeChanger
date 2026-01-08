# Object-Oriented Architecture

## Overview

The JobResumeChanger application has been refactored to follow object-oriented programming (OOP) principles and design patterns. This document explains the architectural decisions and patterns implemented.

## Architecture Layers

### 1. Service Layer

The service layer encapsulates business logic and follows the Single Responsibility Principle.

#### ResumeService
**Purpose**: Handles all resume-related operations

**Responsibilities**:
- Resume file validation and upload
- Integration with parser, analyzer, and comparison modules
- Resume generation coordination
- File operations management

**Key Methods**:
```python
- process_resume_upload(file, job_description) -> Dict
- search_suggestions(point) -> list
- generate_updated_resume(resume_data, added_points, ...) -> str
- is_allowed_file(filename) -> bool
- validate_file_exists(filepath) -> bool
```

**OOP Principles Applied**:
- **Encapsulation**: Hides implementation details of file handling and module coordination
- **Composition**: Composes ResumeParser, JobAnalyzer, ComparisonEngine, etc.
- **Single Responsibility**: Only handles resume operations

#### SessionService
**Purpose**: Manages user session state

**Responsibilities**:
- Session initialization and lifecycle
- Session data storage and retrieval
- Point management (add/get)
- Session status tracking

**Key Methods**:
```python
- initialize_session(session_id, resume_data, ...) -> None
- add_point(point, section, project, additional_info) -> Dict
- get_resume_data() -> Optional[Dict]
- get_added_points() -> list
- get_status() -> Dict
```

**OOP Principles Applied**:
- **Encapsulation**: Abstracts session storage implementation
- **Information Hiding**: Internal session structure hidden from controllers
- **Single Responsibility**: Only manages session state

### 2. Controller Layer

#### ResumeController
**Purpose**: Handles HTTP requests and coordinates services

**Responsibilities**:
- Request validation
- Service orchestration
- Response formatting
- Error handling

**Key Methods**:
```python
- upload() -> Tuple[dict, int]
- search_point() -> Tuple[dict, int]
- add_point() -> Tuple[dict, int]
- generate_resume() -> Tuple[dict, int]
- download() -> Response
- get_status() -> Tuple[dict, int]
```

**OOP Principles Applied**:
- **Dependency Injection**: Services are injected via constructor
- **Separation of Concerns**: Separates HTTP handling from business logic
- **Single Responsibility**: Only handles request/response coordination

### 3. Configuration Layer

#### ApplicationConfig
**Purpose**: Centralizes application configuration

**Responsibilities**:
- Configuration management
- Environment-based settings
- Secret key validation

**OOP Principles Applied**:
- **Encapsulation**: Configuration logic in one place
- **Single Responsibility**: Only manages configuration

### 4. Application Layer

#### JobResumeChangerApp
**Purpose**: Main application orchestrator

**Responsibilities**:
- Flask app initialization
- Service instantiation
- Route registration
- Application lifecycle management

**Key Methods**:
```python
- _configure_app() -> None
- _initialize_services() -> None
- _register_routes() -> None
- run(host, port) -> None
```

**OOP Principles Applied**:
- **Factory Pattern**: create_app() factory function
- **Dependency Injection**: Config injected into app
- **Composition**: Composes services and controllers
- **Single Responsibility**: Manages application lifecycle

## Design Patterns Implemented

### 1. Service Layer Pattern
Separates business logic from presentation and data access layers.

**Benefits**:
- Reusable business logic
- Easier testing (can mock services)
- Clear separation of concerns

### 2. Dependency Injection
Services and dependencies are passed to objects rather than created internally.

**Example**:
```python
controller = ResumeController(resume_service, session_service)
```

**Benefits**:
- Loose coupling
- Easy to test with mock objects
- Flexible configuration

### 3. Controller Pattern
Mediates between views (routes) and business logic (services).

**Benefits**:
- Thin routes
- Testable request handling
- Clear responsibility boundaries

### 4. Factory Pattern
`create_app()` function creates configured application instances.

**Benefits**:
- Consistent initialization
- Easy to create test instances
- Supports multiple configurations

### 5. Composition over Inheritance
Services compose modules rather than inheriting from them.

**Example**:
```python
class ResumeService:
    def __init__(self, ...):
        self.resume_parser = ResumeParser()
        self.job_analyzer = JobAnalyzer()
        # ... other modules
```

**Benefits**:
- Flexible relationships
- Easier to change implementations
- Better encapsulation

## SOLID Principles

### Single Responsibility Principle (SRP)
Each class has one reason to change:
- `ResumeService`: Resume operations
- `SessionService`: Session management
- `ResumeController`: Request handling
- `ApplicationConfig`: Configuration

### Open/Closed Principle (OCP)
Classes are open for extension but closed for modification:
- Services can be extended by inheritance
- New services can be added without modifying existing code

### Liskov Substitution Principle (LSP)
Services implement clear contracts and can be substituted:
- Any service following the interface can replace current implementations

### Interface Segregation Principle (ISP)
Services expose focused interfaces:
- Services only expose methods relevant to their responsibility
- No bloated interfaces

### Dependency Inversion Principle (DIP)
High-level modules don't depend on low-level modules:
- Controller depends on service abstractions, not implementations
- Services can be mocked or replaced

## Class Diagram

```
┌─────────────────────┐
│ ApplicationConfig   │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────────────┐
│ JobResumeChangerApp         │
├─────────────────────────────┤
│ - config: ApplicationConfig │
│ - app: Flask                │
│ - resume_service: Service   │
├─────────────────────────────┤
│ + run()                     │
│ - _configure_app()          │
│ - _initialize_services()    │
│ - _register_routes()        │
└──────────┬──────────────────┘
           │
           ↓
┌─────────────────────────────┐
│ ResumeController            │
├─────────────────────────────┤
│ - resume_service: Service   │
│ - session_service: Service  │
├─────────────────────────────┤
│ + upload()                  │
│ + search_point()            │
│ + add_point()               │
│ + generate_resume()         │
│ + download()                │
│ + get_status()              │
└──────────┬──────────────────┘
           │
           ├────────────────────────┐
           ↓                        ↓
┌─────────────────────┐  ┌─────────────────────┐
│ ResumeService       │  │ SessionService      │
├─────────────────────┤  ├─────────────────────┤
│ - resume_parser     │  │ - session           │
│ - job_analyzer      │  ├─────────────────────┤
│ - comparison_engine │  │ + initialize_...()  │
│ - web_search_engine │  │ + add_point()       │
│ - resume_generator  │  │ + get_resume_data() │
├─────────────────────┤  │ + get_status()      │
│ + process_resume_..()  └─────────────────────┘
│ + search_...()      │
│ + generate_...()    │
└─────────────────────┘
```

## Testing Benefits

The OOP architecture makes testing easier:

1. **Unit Testing Services**:
```python
service = ResumeService('uploads', 'processed', {'pdf'})
result = service.is_allowed_file('test.pdf')
assert result == True
```

2. **Mocking Dependencies**:
```python
mock_service = Mock(ResumeService)
controller = ResumeController(mock_service, session_service)
```

3. **Integration Testing**:
```python
config = ApplicationConfig()
app = JobResumeChangerApp(config)
# Test full application flow
```

## Migration Guide

### Before (Procedural)
```python
@app.route('/upload', methods=['POST'])
def upload():
    parser = ResumeParser()
    result = parser.parse(file)
    # ... inline business logic
```

### After (OOP)
```python
@app.route('/upload', methods=['POST'])
def upload():
    controller = ResumeController(resume_service, session_service)
    return controller.upload()
```

## Benefits Summary

1. **Maintainability**: Clear structure, easy to locate code
2. **Testability**: Services can be tested in isolation
3. **Scalability**: Easy to add new features
4. **Reusability**: Services can be used in different contexts
5. **Flexibility**: Easy to swap implementations
6. **Readability**: Clear responsibilities and relationships

## Future Enhancements

The OOP architecture supports:
- Adding new service types (e.g., AuthService, CacheService)
- Implementing interfaces for service contracts
- Adding middleware layers
- Supporting multiple storage backends
- Implementing async operations
- Adding service decorators for logging, caching, etc.
