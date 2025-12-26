# GitHub MCP tool list

## Repo and files
- create_or_update_file: create/update one file (requires `sha` for update)
- push_files: push multiple files in one commit
- get_file_contents: read file/dir contents
- create_branch: create a new branch
- list_commits: list commits for a branch
- create_repository: create a new repository
- fork_repository: fork a repository

## Issues
- create_issue
- list_issues
- get_issue
- update_issue
- add_issue_comment
- search_issues

## Pull requests
- create_pull_request
- list_pull_requests
- get_pull_request
- get_pull_request_files
- get_pull_request_status
- get_pull_request_comments
- get_pull_request_reviews
- create_pull_request_review
- update_pull_request_branch
- merge_pull_request

## Search
- search_repositories
- search_code
- search_users

# Search query syntax reminders

## Code search
- language:javascript
- repo:owner/name
- path:app/src
- extension:js
Example: q: "import express" language:typescript path:src/

## Issue/PR search
- is:issue or is:pr
- is:open or is:closed
- label:bug
- author:username
Example: q: "memory leak" is:issue is:open label:bug

## User search
- type:user or type:org
- followers:>1000
- location:London
Example: q: "fullstack developer" location:London followers:>100
