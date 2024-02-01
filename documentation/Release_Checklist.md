# Codename: Empty Release Checklist

## Purpose

The purpose of this document is to provide a checklist of tasks to be completed before a release of the Empty project. This will help ensure that all necessary tasks are completed.

## Confirmations

Prior to setting up a release, the following confirmations should be made:

- [ ] All related issues (to this release) are closed
- [ ] No outstanding pull requests (to this release) are open
- [ ] Git has no Pull Request conflicts

## Release Checklist

### 1. Pre-Compile

- [ ] Create a new branch for release actions
- [ ] Update version numbers
    - [ ] Update version number in "main.py"
    - [ ] Update version number in "settings.json"
    - [ ] Update version number in "meta.json" for "official" data pack 
    - [ ] Update version number in "meta.json" for "officialModOne" data pack
- [ ] All documentation is up to date
- [ ] Confirm all settings are put back to their default values
- [ ] Confirm that all "meta.json" files are not in a development state
- [ ] Confirm all developer code that could be displaying information to the player is removed
- [ ] Write release notes

### 2. Compile

- [ ] Checkout the release branch
- [ ] For Windows, run "compile.py" to compile the project
    - [ ] Ensure that the .exe properly runs
    - [ ] Ensure that all resource files were properly copied
    - [ ] Commit the compiled files
- [ ] If doing a Mac release, run compile on a Mac
    - [ ] First fetch the windows compile commit
    - [ ] Ensure that the .app properly runs
    - [ ] Ensure that all resource files were properly copied
    - [ ] Commit the compiled files

### 3. Post-Compile

- [ ] Test the Windows release
    - [ ] Ensure that the .exe properly runs
    - [ ] Ensure that the game can be properly played without any crashes
- [ ] Test the Mac release
    - [ ] Ensure that the .app properly runs
    - [ ] Ensure that the game can be properly played without any crashes
- [ ] Do the Pull Request to merge release branch into main
    - [ ] First create PR to merge release branch into dev
        - [ ] Delete the release branch
    - [ ] Then create PR to merge dev into main
        - [ ] Add release notes to the PR
        - [ ] Delete the dev branch
        - [ ] Create a new dev branch for future development
- [ ] Confirm that the release is properly merged into main
