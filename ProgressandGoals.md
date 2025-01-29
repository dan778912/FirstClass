# Project Progress and Goals

## What was already completed
### General

We have functionality in creating a title, masthead page, an about page. Within those pages, we have some implemention on People, Text, and Manuscripts. As per the requirements of last semester,
we have communication enabled with both the cloud and local version of our database.
### People
We already have basic CRUD functionality, without much granularity in terms of who can do what, as well as tests that cover the basic cases and a few edge.

### Text
Basic CRUD functionality already exists, and corresponding tests. Similar to the People class, we have no distinction between which roles can edit text and which roles cannot.

### Manuscripts
We have some basic functionality but lack components that complete the FSM shown in the diagram, such as which roles can do what.

## Goals for this semester

### Backend things
#### People

- [ ] Limitations on account editing, creation, deletion, etc.
- [ ] Restrictions and functionality in how roles are assigned
    - [ ] Submitting a manuscript creates author role
    - [ ] Assigning referee manuscript creates referee role (for that person)
- [ ] Restrictions on which accounts can view what
    - [ ] All manuscripts only on editor and managing editors
    - [ ] All people only on editor and managing editor

### Frontend things
#### General requirements
- [ ] Masthead page pulled from backend
- [ ] About page
- [ ] Submissions guidelines page
- [ ] Account credentials and functionality
    - [ ] Log in
    - [ ] Sign up
    - [ ] Edit account
    - [ ] Delete account
- [ ] Clean visualization for all people
- [ ] Dashboard for manuscripts

## Additional comments
This advanced goal might be fun to accomplish if times allows (and with the incentive of extra credit :eyes:)
- [ ] Advanced: record a history of each user's interacitons with the system.

## Links 
* [Link to user requirements](https://github.com/gcallah/SoftwareEngineering/blob/master/docs/user_reqs_spring_2025.md)
* [Link to manuscript FSM](https://github.com/AthenaKouKou/journal/blob/main/docs/Manuscript_FSM.jpg)
* [Link to README](README.md)
