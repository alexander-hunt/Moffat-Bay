# Moffat Bay Lodge

## Module 6 Test Plan

**Project:** Moffat Bay Lodge  
**Course:** Capstone in Software Development  
**Description:** Six manual functional tests for the authenticated room-reservation workflow.  
**Date:** (09/07/2026)  
**Version:** v1.1

## Test Completion Tracker

- Test 1 — Authenticated customer opens the reservation page
- Test 2 — Valid stay produces an accurate reservation summary
- Test 3 — Reservation rejects a guest count over room capacity
- Test 4 — Reservation rejects invalid date order
- Test 5 — Cancel discards a pending reservation
- Test 6 — Confirmation saves exactly one reservation

## Module Deliverable Tracker

- Complete all tests
- Zip up the code repository and the completed Module Test Plan Document.

## Test 1: Authenticated customer opens the reservation page

**Test complete**

**Test Objective:** Verify that booking requires login and that an authenticated customer can view the active room catalog.

**Peer tester:** Alexander Hunt  
**Date tested:** (09/07/2026)

| Step | Action | Expected results | Developer pass/fail | Tester pass/fail | Screenshot/evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | Open /reservations/book in a private browser while logged out. | The browser redirects to /account; the booking form is not displayed. | Pending | Pass + Screenshotted | Screenshot for Step 1 |
| 2 | Log in with a valid development customer account. | Login succeeds and the authenticated navigation displays Book and My stays. | Pending | Pass + Screenshotted | Screenshot for Step 2 |
| 3 | Open /reservations/book. | The Book your stay page loads without a server error. | Pending | Pass + Screenshotted | Screenshot for Step 3 |
| 4 | Review the Room list. | Only active rooms appear, each with its server-provided nightly rate. | Pending | Pass + Screenshotted | Screenshot for Step 4 |
| 5 | Review the remaining fields. | Number of guests, check-in date, check-out date, and Review reservation are present. | Pending | Pass + Screenshotted | Screenshot for Step 5 |

### Comments

The reservations/book page redirects a user that is not logged in to the login page successfully. A valid login flow is present and the reservations/book page loads for a logged in user. The room list looks correct with it’s unique naming conventions and adjusted pricings. All reservation fields are present.

### Screenshots

- Step 1
- Step 2
- Step 3
- Step 4
- Step 5

## Test 2: Valid stay produces an accurate reservation summary

**Test complete**

**Test Objective:** Verify room selection, date calculation, and server-authoritative pricing for a valid stay.

**Developer:** Justin Morrow  
**Date tested:** (mm/dd/yyyy)  
**Peer tester:** Carli McAvoy  
**Date tested:** (mm/dd/yyyy)

| Step | Action | Expected results | Developer pass/fail | Tester pass/fail | Screenshot/evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | Log in and open /reservations/book. | The reservation form loads with active room choices. | Pending | Pending + screenshot | Screenshot for Step 1 |
| 2 | Select a room, enter a guest count within capacity, and choose a three-night stay. | The form accepts all values without validation errors. | Pending | Pending + screenshot | Screenshot for Step 2 |
| 3 | Click Review reservation. | The browser opens /reservations/summary. | Pending | Pending + screenshot | Screenshot for Step 3 |
| 4 | Compare the summary with the submitted room, guests, and dates. | All selected details and three nights are displayed correctly. | Pending | Pending + screenshot | Screenshot for Step 4 |
| 5 | Calculate the expected total from the displayed nightly rate. | The displayed total equals nightly rate multiplied by three; no reservation is saved yet. | Pending | Pending + screenshot | Screenshot for Step 5 |

### Comments

Pending execution. Record 2–3 substantive sentences with observed behavior, defects, and constructive feedback after developer and peer testing.

## Test 3: Reservation rejects a guest count over room capacity

**Test complete**

**Test Objective:** Verify that the booking form enforces the selected room's maximum guest capacity.

**Developer:** Justin Morrow  
**Date tested:** (mm/dd/yyyy)  
**Peer tester:** Noor Al Salihi  
**Date tested:** (mm/dd/yyyy)

| Step | Action | Expected results | Developer pass/fail | Tester pass/fail | Screenshot/evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | Log in and open /reservations/book. | The reservation form and room choices load. | Pending | Pending + screenshot | Screenshot for Step 1 |
| 2 | Select a room and note its supported capacity from the test data. | A valid active room is selected. | Pending | Pending + screenshot | Screenshot for Step 2 |
| 3 | Enter a guest count greater than that room's maximum and valid stay dates. | The form retains the submitted values. | Pending | Pending + screenshot | Screenshot for Step 3 |
| 4 | Click Review reservation. | The page remains on the booking form with an accommodation-capacity error. | Pending | Pending + screenshot | Screenshot for Step 4 |
| 5 | Check the session and reservation table. | No valid pending summary is created and no reservation row is inserted. | Pending | Pending + screenshot | Screenshot for Step 5 |

### Comments

Pending execution. Record 2–3 substantive sentences with observed behavior, defects, and constructive feedback after developer and peer testing.

## Test 4: Reservation rejects invalid date order

**Test complete**

**Test Objective:** Verify checkout must occur after check-in and invalid dates cannot reach the summary.

**Developer:** Justin Morrow  
**Date tested:** (mm/dd/yyyy)  
**Peer tester:** Alexander Hunt  
**Date tested:** (09/07/2026)

| Step | Action | Expected results | Developer pass/fail | Tester pass/fail | Screenshot/evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | Log in and open /reservations/book. | The reservation form loads. | Pending | Pass + Screenshotted | Screenshot for Step 1: reservation form loads for a logged in user |
| 2 | Select an active room and enter a valid guest count. | The room and guest values are accepted. | Pending | Pass + Screenshotted | Screenshot for Step 2: Reservation selection interface functions correctly |
| 3 | Set check-out equal to check-in and submit. | A Check-out must be after check-in error appears. | Pending | Pass + Screenshotted | Screenshot for Step 3: Check-out same day as check-in got an error |
| 4 | Set check-out before check-in and submit again. | The same date-order rule blocks the request. | Pending | Pass + Screenshotted | Screenshot for Step 4: Check-out before check-in got an error |
| 5 | Confirm the result. | No summary is shown and no reservation row is inserted. | Pending | Pass + Screenshotted | Screenshot for Step 5: Reservation was blocked |

### Comments

A logged in user is able to view the reservations and booking page. The active room navigation and guest count selection input fields work as expected. Check-out and check-in time validations block invalid booking times. The database backend was also not updated in the error cases as expected.

## Test 5: Cancel discards a pending reservation

**Test complete**

**Test Objective:** Verify Cancel returns to booking and does not persist the reviewed reservation.

**Developer:** Justin Morrow  
**Date tested:** (mm/dd/yyyy)  
**Peer tester:** Carli McAvoy  
**Date tested:** (mm/dd/yyyy)

| Step | Action | Expected results | Developer pass/fail | Tester pass/fail | Screenshot/evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | Create a valid stay selection and click Review reservation. | The reservation summary displays the pending stay. | Pending | Pending + screenshot | Screenshot for Step 1 |
| 2 | Record the current reservation-table row count. | A baseline count is available for comparison. | Pending | Pending + screenshot | Screenshot for Step 2 |
| 3 | Click Cancel on the summary. | The browser returns to /reservations/book with a cancellation message. | Pending | Pending + screenshot | Screenshot for Step 3 |
| 4 | Attempt to open /reservations/summary directly. | The app redirects to booking because no valid pending reservation remains. | Pending | Pending + screenshot | Screenshot for Step 4 |
| 5 | Query the reservation table again. | The row count is unchanged; the cancelled stay was not saved. | Pending | Pending + screenshot | Screenshot for Step 5 |

### Comments

Pending execution. Record 2–3 substantive sentences with observed behavior, defects, and constructive feedback after developer and peer testing.

## Test 6: Confirmation saves exactly one reservation

**Test complete**

**Test Objective:** Verify explicit confirmation persists one customer-owned reservation and prevents a duplicate repeat submission.

**Developer:** Justin Morrow  
**Date tested:** (mm/dd/yyyy)  
**Peer tester:** Noor Al Salihi  
**Date tested:** (mm/dd/yyyy)

| Step | Action | Expected results | Developer pass/fail | Tester pass/fail | Screenshot/evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | Create and review a valid pending reservation while logged in. | The summary displays server-recalculated stay details and total. | Pending | Pending + screenshot | Screenshot for Step 1 |
| 2 | Click Confirm reservation. | The app redirects to a confirmation page with a reservation ID. | Pending | Pending + screenshot | Screenshot for Step 2 |
| 3 | Review the confirmation details. | Room, guests, dates, nights, and total match the reviewed stay. | Pending | Pending + screenshot | Screenshot for Step 3 |
| 4 | Query MySQL for the displayed reservation ID. | Exactly one row exists and is linked to the signed-in customer. | Pending | Pending + screenshot | Screenshot for Step 4 |
| 5 | Submit the confirm endpoint again or refresh the completed flow. | No second reservation is created; the user is directed to start a valid booking. | Pending | Pending + screenshot | Screenshot for Step 5 |

### Comments

Pending execution. Record 2–3 substantive sentences with observed behavior, defects, and constructive feedback after developer and peer testing.