# FYDP Progress Tracker - Quick Start Guide

## Running the Application

1. Open a terminal/command prompt
2. Navigate to the project directory:
   ```
   cd "c:\CODE\FYDP Progress"
   ```
3. Run the application:
   ```
   python main.py
   ```

## First-Time Setup

The application will automatically:
- Create the SQLite database file (`fydp_tracker.db`)
- Set up all necessary tables
- Display the dashboard

## Navigation

Use the sidebar menu to navigate between sections:
- **Dashboard** - Overview of your progress
- **Tasks** - Manage your project tasks
- **Learning Log** - Document your learning journey
- **Milestones** - Track project milestones
- **Reports** - Create progress reports
- **Documents** - Manage project documents
- **Supervisor Notes** - Record meeting notes
- **Research References** - Organize research materials

## Common Operations

### Adding a Task
1. Click "Tasks" in the sidebar
2. Fill in the form at the bottom:
   - Title (required)
   - Description
   - Start Date (YYYY-MM-DD)
   - Deadline (YYYY-MM-DD)
   - Status (Not Started, In Progress, Completed, Blocked)
   - Phase (FYDP1, FYDP2, FYDP3)
3. Click "Add Task"

### Updating a Record
1. Select the item from the list
2. Modify the details in the form
3. Click "Update [Type]"

### Deleting a Record
1. Select the item from the list
2. Click "Delete [Type]"
3. Confirm the deletion

### Searching
1. Enter your search term in the search box
2. Click "Search"
3. Click "Clear" to show all records

### Exporting to CSV
1. Navigate to Tasks, Learning Log, or Milestones
2. Click "Export CSV"
3. Choose a location to save the file

## Tips for Effective Use

### Task Management
- Set realistic deadlines
- Update task status regularly
- Use the "Blocked" status when you encounter obstacles
- Filter by phase to focus on current work

### Learning Log
- Make entries regularly (daily or weekly)
- Use tags for easy categorization (e.g., "python, database, gui")
- Include source information for future reference
- Note how each learning relates to your project

### Milestones
- Define clear expected outputs
- Update actual outputs as you complete them
- Use comments to note any deviations or insights
- Track submission dates carefully

### Progress Reports
- Create reports weekly or after major work sessions
- Be honest about problems faced
- Document time spent for project tracking
- Use next action to plan your upcoming work

### Document Management
- Track all project deliverables
- Maintain version numbers
- Update file paths when documents move
- Use submission status to track deliverable states

### Supervisor Notes
- Record notes immediately after meetings
- List all assigned tasks clearly
- Review before next meeting
- Use search to find previous discussions

### Research References
- Add references as you find them
- Write summaries while the content is fresh
- Note relevance to help prioritize reading
- Include DOI or stable URLs when available

## Date Format

Always use YYYY-MM-DD format for dates:
- Correct: 2025-11-16
- Incorrect: 11/16/2025 or 16-11-2025

## Dashboard Features

The dashboard shows:
- Total tasks count
- Completed tasks count
- Pending tasks count
- Progress percentage (with visual progress bar)
- Upcoming deadlines table

Click "Refresh Dashboard" to update statistics after making changes in other sections.

## Data Backup

Important: Regularly backup your database file!

The database file is located at:
```
c:\CODE\FYDP Progress\fydp_tracker.db
```

Recommended backup schedule:
- Daily: If actively using
- Weekly: During active project phases
- Before major changes or updates

## Troubleshooting

### Application won't start
- Ensure Python 3.x is installed
- Check that you're in the correct directory
- Verify all project files are present

### Database errors
- Check if `fydp_tracker.db` is not locked by another process
- Ensure you have write permissions in the directory
- Try deleting the database file to start fresh (you'll lose data)

### Display issues
- Ensure your screen resolution is at least 1024x768
- Try maximizing the window
- Check Tkinter is properly installed with Python

## Keyboard Shortcuts

- Tab: Navigate between fields
- Enter: Submit form (in most single-line inputs)
- Esc: Close message boxes
- Click: Select items from lists

## Best Practices

1. **Regular Updates**: Update your progress daily or weekly
2. **Consistent Naming**: Use clear, descriptive titles
3. **Tag Everything**: Use tags in learning logs for better organization
4. **Export Regularly**: Create CSV exports for reporting
5. **Review Dashboard**: Check progress weekly
6. **Clean Data**: Remove or archive old/irrelevant items
7. **Backup Often**: Keep your data safe

## Getting Help

If you encounter issues:
1. Check this guide first
2. Review the README.md file
3. Check the database.py file for database structure
4. Verify all files are in correct locations

## Project Organization

Organize your work by FYDP phase:
- **FYDP1**: Planning, research, initial design
- **FYDP2**: Implementation, testing, refinement
- **FYDP3**: Final implementation, documentation, presentation

Use the phase filters to focus on current work while tracking future items.
