# mdBook Indexer

# Using this action

To use this action create or expand an existing workflow.yaml
```yaml
name: Test Action
on:
    push:
        branches: [main]
    pull_request:
        branches: [main]
    workflow_dispatch:

jobs:
    get-num-square:
      runs-on: ubuntu-latest
      name: Testing functionality
      steps:
        - name: Checkout
          uses: actions/checkout@v2
        - name: Index mdBook 
          id: mdBook_site_to_JSON
          uses: EzioTheDeadPoet/actions-mdBook-indexer@v1.1
          with:
            mdBook_url: https://wiki.wabbajack.org/ # URL to the hosted mdBook
            output_file: example_output.json # Desired output name (optional with default: mdBook_index.json)
        - name: Deploy Data # To write the index into a repository that can be addressed by 3rd party applications
          uses: peaceiris/actions-gh-pages@v3
          with:
            github_token: ${{ secrets.GITHUB_TOKEN }}
            publish_dir: ./json_index # the path the where this action will put it's files
            publish_branch: index_json
```
