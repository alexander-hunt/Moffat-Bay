# Capstone in Software Development

> Persistent course data and reusable reference for course assignments and project work.

## Course and Team

| Item | Details |
| --- | --- |
| Course | Capstone in Software Development |
| Instructor | Christine Mazhata |
| Group | Group B |
| Team leader | Alexander Hunt |
| Team members | Alexander Hunt, Justin Morrow, Noor Al Salihi, Carli McAvoy |
| Technical stack | Python and MySQL |

## Project Prompt: Moffat Bay Lodge

### Joviedsa Island, Washington State

Six months ago, the San Juan Islands First Nations Development Committee approved building a resort and marina at Moffat Bay on Joviedsa Island. Construction of both facilities is almost complete. The committee has hired the team to complete one of the two projects required before the facilities open.

### Project 1: Moffat Bay Lodge

Build a website that supports the following workflow:

- Visitors can view every aspect of the Lodge website without logging in.
- Customers must log in or register for a free account before submitting a lodge reservation.
- Payment processing is not required, but customers must click a button to confirm their reservation.
- After confirmation, the reservation must be inserted into the database.
- Stored reservations populate the Reservation Lookup page.
- Registered users must be saved in a database table and validated during login.

## Project Requirements

### Public Pages

| Page | Requirement |
| --- | --- |
| Landing Page | A simple marketing landing page. Use the Internet for landing-page inspiration. |
| About Us | Static HTML/CSS content related to Moffat Bay Lodge. |
| Contact Us | Static HTML/CSS content related to Moffat Bay Lodge. |
| Attractions | Static HTML/CSS content about island activities. Include hiking, kayaking, whale watching, and scuba diving. |

### Registration

The Registration page must collect, at minimum:

- Email address
- First name
- Last name
- Telephone
- Password

Additional requirements:

- Assign every customer a unique `customerId`.
- Use the email address as the username.
- Require passwords to have at least eight characters, one number, one uppercase letter, and one lowercase letter.
- Validate email addresses against a standard format, such as `bob@something.com`.
- Hash or encrypt passwords using standard security practices. Cite any external authors whose code is reused.

### Login and Session

- Provide email-address (username) and password fields.
- Add logged-in customers to the application session.

### Lodge Reservation: Book Your Vacation

Save lodge reservations to MySQL. The form must provide selections for room size, number of guests, and check-in/check-out dates.

| Room configuration | Nightly rate |
| --- | ---: |
| Double full beds | $120.00 |
| Queen | $135.00 |
| Double queen beds | $150.00 |
| King | $160.00 |

### Reservation Summary

- Display a reservation confirmation summary.
- Provide buttons to cancel or submit the reservation.
- Save submitted reservations to MySQL.
- Return customers who cancel to the hotel reservation page.

### Reservation Lookup

Provide a field that searches by reservation ID or email address and displays a reservation summary containing the room size, number of guests, and check-in/check-out dates.

## Module 1: TDD Assignment

Build the technical design document (TDD) for the Moffat Bay project.

### TDD Structure

1. Introduction
   1. Purpose
   2. Terminology
   3. User Personas
   4. User Stories
   5. Work Estimations (To-Do List)
2. Design
   1. Prototypes
   2. ERD
3. QA Testing
   1. QA Test Plan

### Instructions

1. Draft a TDD with at least three user personas and nine user stories (three stories per persona). Prioritize the stories; break the top three into steps with story hours. Determine team To-Do tasks and provide them to the team leader for the Kanban board by the end of the week.
2. Use the structure above. Leave Design and QA Testing blank for now; they are completed in later modules.

### Deliverables

1. Purpose
2. Terminology
3. User personas
4. User stories
5. Work estimations (To-Do List) posted to the team Kanban board

## Module 2: Prototype Assignment

Create functional prototypes for every project website page and a landing-page mockup.

1. Create a realistic, high-fidelity landing-page mockup including color, layout, and font selection.
2. Update the team Kanban board by the end of the week.
3. Zip the prototype and mockup files for submission.
4. The team leader must arrange prototype and mockup approval.

## Module 3: ERD Assignment

1. Create an entity-relationship diagram (ERD) for the Moffat Bay project. Include as much detail as possible to support database creation.
2. Update the team Kanban board by the end of the week.

## Module 4: Database Development Assignment

1. Create and populate SQL files. Every table must include all ERD attributes and at least three entries.
2. Ensure tables match the ERD. Submit a revised ERD if the table design changes.
3. Run `SELECT * FROM xxx;` for each table to display its contents.
4. Take screenshots of each result.
5. Update the team Kanban board by the end of the week.

### Deliverable

Combine all screenshots in one Word document that includes your name, date, and assignment number.

## Modules 5-9

| Module | Team deliverables |
| --- | --- |
| 5 | Landing page and backend code; Login page and backend code; User Registration page and backend code; update Kanban board. |
| 6 | Room Reservation page and backend code; update Kanban board. |
| 7 | About Us page and backend code; Reservation Summary page and backend code; update Kanban board. |
| 8 | Contact Us page and backend code; Reservation Lookup page and backend code; update Kanban board. |
| 9 | Attractions page and backend code; update Kanban board. |

## Project To-Do Reference

> Persistent implementation backlog. Update task ownership and status as team decisions are made.

### TD-01: Project Setup

| Field | Value |
| --- | --- |
| Priority | High |
| Estimate | 3 hours |
| Suggested owner | Team leader / Developer |
| Related stories | US-01 through US-09 |

Create the shared project skeleton, repository structure, development conventions, and environment configuration.

**Acceptance criteria**

- Shared project structure is available to the team.
- Python and MySQL configuration requirements are documented.
- Naming and coding conventions are established.
- Required dependencies are identified.
- Each team member can access and run the initial project.

### TD-02: Database Setup

| Field | Value |
| --- | --- |
| Priority | High |
| Estimate | 5 hours |
| Suggested owner | Database Developer |
| Related stories | US-01, US-03, US-06 |

Create the MySQL customer and reservation tables, including primary keys, foreign keys, constraints, and test data.

**Acceptance criteria**

- Every customer receives a unique customer ID.
- Customer email addresses are unique.
- Password hashes can be stored securely.
- Every reservation receives a unique reservation ID.
- Each reservation is related to a registered customer.
- Room, guest-count, date, rate, and total fields are supported.
- Seed or test records are available.

### TD-03: Public Website Pages

| Field | Value |
| --- | --- |
| Priority | Low |
| Estimate | 8 hours |
| Suggested owner | Front-End Developer |
| Related story | US-05 |

Build responsive Landing, About Us, Contact Us, and Attractions pages.

**Acceptance criteria**

- All four pages are available without logging in.
- The landing page provides a clear introduction and booking call to action.
- The About Us and Contact Us pages present relevant lodge information.
- The Attractions page includes hiking, kayaking, whale watching, and scuba diving.
- Navigation works between all public pages.
- Pages display correctly on desktop and mobile screens.

### TD-04: Customer Registration

| Field | Value |
| --- | --- |
| Priority | High |
| Estimate | 11 hours |
| Suggested owner | Full-Stack Developer |
| Related story | US-01 |

Implement registration with required contact fields, validation, unique-email handling, password hashing, and MySQL persistence.

**Acceptance criteria**

- The form collects email, first name, last name, telephone, and password.
- Required fields and standard email format are validated on the server.
- Passwords require at least eight characters, one uppercase letter, one lowercase letter, and one number.
- Passwords are hashed before storage.
- Duplicate email addresses are rejected with a clear message.
- A unique customer ID is assigned after successful registration.

### TD-05: Registration Testing

| Field | Value |
| --- | --- |
| Priority | High |
| Estimate | 2 hours |
| Suggested owner | QA / Developer |
| Related story | US-01 |

Test the complete registration workflow, including successful and unsuccessful submissions.

**Acceptance criteria**

- Required-field, email-format, and password-policy validation are tested.
- Duplicate-email handling is tested.
- Successful MySQL insertion is verified.
- Passwords are confirmed not to be stored as plaintext.
- Results and discovered defects are documented.

### TD-06: Login and Session Management

| Field | Value |
| --- | --- |
| Priority | High |
| Estimate | 8 hours |
| Suggested owner | Back-End Developer |
| Related story | US-02 |

Implement email-and-password login, password-hash verification, authenticated sessions, logout, and reservation-submission protection.

**Acceptance criteria**

- Customers can log in using their email address and password.
- The submitted password is checked against the stored hash.
- Successful login creates an authenticated application session.
- Invalid credentials produce a clear, nonsensitive error.
- Customers can log out and end their session.
- Unauthenticated users cannot confirm or submit reservations and are directed to login or registration.

### TD-07: Login and Session Testing

| Field | Value |
| --- | --- |
| Priority | High |
| Estimate | 2 hours |
| Suggested owner | QA / Developer |
| Related story | US-02 |

Test authentication, session persistence, logout, invalid credentials, and reservation access control.

**Acceptance criteria**

- Successful login and incorrect-email/password cases are tested.
- Session persistence and logout are verified.
- Unauthenticated reservation submission is blocked.
- Login or registration redirect behavior is verified.
- Results and defects are documented.

### TD-08: Room and Stay Selection

| Field | Value |
| --- | --- |
| Priority | High |
| Estimate | 5 hours |
| Suggested owner | Front-End Developer |
| Related stories | US-03, US-04 |

Build the reservation form for room configuration, guest count, and stay dates.

**Acceptance criteria**

- The form offers double-full beds at $120, queen at $135, double-queen beds at $150, and king at $160 per night.
- Customers can enter a guest count and select check-in/check-out dates.
- Room rates are clearly visible.
- Invalid or incomplete entries produce helpful messages.

### TD-09: Reservation Business Logic

| Field | Value |
| --- | --- |
| Priority | High |
| Estimate | 6 hours |
| Suggested owner | Back-End Developer |
| Related stories | US-03, US-08 |

Implement reservation validation, stay and price calculations, customer relationships, and reservation ID creation.

**Acceptance criteria**

- Only recognized room options and rates are accepted.
- Guest count is validated and checkout occurs after check-in.
- Nights and total cost are calculated correctly.
- Reservations are associated with the authenticated customer and receive unique IDs.
- Server-side validation blocks manipulated or invalid submissions.

### TD-10: Reservation Summary and Confirmation

| Field | Value |
| --- | --- |
| Priority | High |
| Estimate | 4 hours |
| Suggested owner | Full-Stack Developer |
| Related stories | US-03, US-07, US-08, US-09 |

Build the summary page with cancellation and confirmation. Save only after explicit confirmation.

**Acceptance criteria**

- The summary displays room size/rate, guest count, dates, nights, and total cost.
- Cancel returns to the reservation form without saving.
- Confirm inserts the reservation into MySQL and displays its ID.
- Refreshing or repeating confirmation does not create duplicates.

### TD-11: Reservation Workflow Testing

| Field | Value |
| --- | --- |
| Priority | High |
| Estimate | 3 hours |
| Suggested owner | QA / Developer |
| Related story | US-03 |

Test room pricing, date and guest validation, calculations, cancellation, confirmation, and persistence.

**Acceptance criteria**

- All four room rates are verified.
- Valid/invalid date ranges and guest counts are tested.
- Night and total-cost calculations are verified.
- Cancel does not save a reservation.
- Confirm inserts the correct MySQL record and returns an ID.
- Results and defects are documented.

### TD-12: Reservation Lookup

| Field | Value |
| --- | --- |
| Priority | Medium |
| Estimate | 6 hours |
| Suggested owner | Full-Stack Developer |
| Related story | US-06 |

Create a page that searches confirmed reservations by reservation ID or customer email.

**Acceptance criteria**

- One search field accepts a reservation ID or email address.
- Matching confirmed reservations are retrieved from MySQL.
- Results show room size, guest count, and check-in/check-out dates.
- A clear no-results message is shown.
- Multiple reservations for an email are presented in a simple list.

### TD-13: Reservation Lookup Testing

| Field | Value |
| --- | --- |
| Priority | Medium |
| Estimate | 2 hours |
| Suggested owner | QA / Developer |
| Related story | US-06 |

Test valid, invalid, matching, and nonmatching reservation searches.

**Acceptance criteria**

- Valid reservation-ID and email searches are tested.
- Multiple results for one email are tested.
- Nonexistent IDs, emails with no reservations, and empty or invalid input are tested.
- Displayed details are checked against MySQL records.
- Results and defects are documented.

### TD-14: Workflow Integration and Usability Review

| Field | Value |
| --- | --- |
| Priority | Medium |
| Estimate | 5 hours |
| Suggested owner | Whole Team |
| Related stories | All |

Connect required pages and verify end-to-end workflows.

**Acceptance criteria**

- Navigation connects public and account pages.
- Visitors can access all public information without logging in.
- Registration and login lead into booking.
- Authenticated customers can complete booking and confirmation.
- Lookup retrieves stored reservation information.
- Forms have clear labels and error messages and remain usable on common desktop and mobile widths.
- Existing required workflows continue to work after integration.

### TD-15: Documentation and Submission Review

| Field | Value |
| --- | --- |
| Priority | Medium |
| Estimate | 4 hours |
| Suggested owner | Team Leader / Whole Team |
| Related stories | All user stories |

Review requirements, update the TDD and Kanban board, document external sources, and prepare the project for submission or demonstration.

**Acceptance criteria**

- The implementation is checked against every project requirement.
- Kanban statuses reflect actual team progress.
- The TDD is updated with approved project information.
- Reused external code and sources are cited.
- Prototype and mockup files are organized for submission.
- The submission package is complete and the team is prepared to demonstrate primary workflows.
- At least one teammate reviews completed work before cards move to Done.