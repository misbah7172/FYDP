# FYDP Progress Tracker

A comprehensive desktop application for tracking Final Year Design Project (FYDP) progress through FYDP1, FYDP2, and FYDP3 phases.

## Features

- **Task Management**: Track tasks with status, deadlines, and FYDP phases
- **Learning Log**: Document daily/weekly learnings with sources and tags
- **Milestone Tracker**: Monitor milestones with expected and actual outputs
- **Progress Reports**: Log work done, problems, and next actions
- **Document Manager**: Track project documents and deliverables
- **Supervisor Notes**: Record meeting notes and assigned tasks
- **Research References**: Manage research papers and resources
- **Dashboard**: View overall progress with statistics and upcoming deadlines
- **CSV Export**: Export tasks, learning logs, and milestones to CSV

## Project Structure

```
FYDP Progress/
├── main.py                 # Application entry point
├── database.py             # Database setup and management
├── models/                 # Data models
│   ├── task.py
│   ├── learning_log.py
│   ├── milestone.py
│   ├── report.py
│   ├── document.py
│   ├── supervisor_note.py
│   └── reference.py
├── controllers/            # Business logic
│   ├── task_controller.py
│   ├── learning_log_controller.py
│   ├── milestone_controller.py
│   ├── report_controller.py
│   ├── document_controller.py
│   ├── supervisor_note_controller.py
│   └── reference_controller.py
└── views/                  # User interface
    ├── dashboard_view.py
    ├── task_view.py
    ├── learning_log_view.py
    ├── milestone_view.py
    ├── report_view.py
    ├── document_view.py
    ├── supervisor_note_view.py
    └── reference_view.py
```

## Requirements

- Python 3.x (tested with Python 3.8+)
- Tkinter (included with Python)
- SQLite3 (included with Python)

## Installation

1. Ensure Python 3.x is installed on your system
2. Navigate to the project directory
3. Run the application:

```bash
python main.py
```

## Usage

### Task Management
- Add tasks with title, description, dates, status, and FYDP phase
- Filter tasks by status or phase
- Search tasks by title or description
- Export tasks to CSV

### Learning Log
- Document what you learned with date, source, and tags
- Add relevance to project notes
- Search logs by content or tags
- Export logs to CSV

### Milestone Tracker
- Track milestones for each FYDP phase
- Record expected vs actual outputs
- Add submission dates and comments
- Filter by phase and export to CSV

### Progress Reports
- Create daily/weekly progress reports
- Log work done, problems faced, and next actions
- Track time spent on tasks
- Search through historical reports

### Document Manager
- Track project documents and deliverables
- Maintain version control
- Record submission status and file paths

### Supervisor Notes
- Record meeting notes from supervisor meetings
- Track assigned tasks from meetings
- Search through meeting history

### Research References
- Manage research papers and resources
- Store links, summaries, and relevance notes
- Search references by title or content

### Dashboard
- View overall task statistics
- Monitor progress percentage with visual progress bar
- See upcoming deadlines
- Quick refresh to update statistics

## Database

The application uses SQLite3 for local data storage. The database file `fydp_tracker.db` is created automatically on first run in the application directory.

### Database Tables
- tasks
- learning_logs
- milestones
- reports
- documents
- supervisor_notes
- references

All tables include appropriate indexes for optimal query performance.

## Features Highlight

- **MVC Architecture**: Clean separation of concerns
- **Input Validation**: Built-in validation for required fields
- **Error Handling**: Comprehensive error messages and confirmations
- **Search Functionality**: Search capability in every section
- **CSV Export**: Export data for tasks, learning logs, and milestones
- **Auto-Save**: All data is saved immediately to the database
- **Date Formatting**: Consistent YYYY-MM-DD date format
- **Status Tracking**: Multiple status options for tasks
- **Phase Tracking**: Support for FYDP1, FYDP2, and FYDP3 phases

## Tips

- Use the date format YYYY-MM-DD for consistency
- Tags in learning logs should be comma-separated
- Regular backups of `fydp_tracker.db` are recommended
- Use the search feature to quickly find specific entries
- Export data regularly for reporting purposes

## License

This is a personal project tool. Feel free to modify and use as needed.
