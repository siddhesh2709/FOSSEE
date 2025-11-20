# 🧪 Testing Checklist

## Pre-Testing Setup

- [ ] Backend server running on http://localhost:8000
- [ ] Web frontend running on http://localhost:3000
- [ ] Desktop app can be launched
- [ ] `sample_equipment_data.csv` file available

---

## 1. Authentication Testing

### Web Application
- [ ] Can access login page at http://localhost:3000
- [ ] Can register new user
- [ ] Registration shows success message
- [ ] Can login with registered credentials
- [ ] Invalid credentials show error message
- [ ] Logout button works
- [ ] After logout, redirects to login page

### Desktop Application
- [ ] Login window appears on launch
- [ ] Can register new user
- [ ] Registration shows success popup
- [ ] Can login with valid credentials
- [ ] Invalid credentials show error
- [ ] Main window opens after successful login
- [ ] Logout closes the application

---

## 2. CSV Upload Testing

### Web Application
- [ ] File input accepts CSV files
- [ ] Browse button works
- [ ] Selected filename is displayed
- [ ] Upload button enabled after file selection
- [ ] Upload shows success message
- [ ] Invalid CSV shows error message
- [ ] File with missing columns shows error
- [ ] Dataset appears in history list

### Desktop Application
- [ ] Browse button opens file dialog
- [ ] Can select CSV file
- [ ] Filename displayed after selection
- [ ] Upload button enabled after selection
- [ ] Upload shows success popup
- [ ] Invalid CSV shows error popup
- [ ] Dataset appears in dropdown

---

## 3. Data Display Testing

### Web Application
- [ ] Data table shows all records
- [ ] Table has correct column headers
- [ ] All 5 columns displayed (Name, Type, Flowrate, Pressure, Temperature)
- [ ] Data matches CSV file
- [ ] Table is scrollable for large datasets
- [ ] Table is responsive on mobile

### Desktop Application
- [ ] Data tab shows table
- [ ] Table has correct headers
- [ ] All records displayed
- [ ] Table is scrollable
- [ ] Columns are resizable
- [ ] Data matches CSV file

---

## 4. Summary Statistics Testing

### Web Application
- [ ] Summary cards display correct counts
- [ ] Average flowrate calculated correctly
- [ ] Average pressure calculated correctly
- [ ] Average temperature calculated correctly
- [ ] Min/max values shown
- [ ] Equipment count is accurate

### Desktop Application
- [ ] Summary tab shows formatted text
- [ ] Total count is correct
- [ ] Equipment type distribution shown
- [ ] All parameter statistics displayed
- [ ] Values match web application

### Verification
Calculate manually from sample data:
- [ ] Total records = 15
- [ ] Equipment types: Pump(4), Compressor(2), Valve(3), HeatExchanger(2), Reactor(2), Condenser(2)
- [ ] Average Flowrate ≈ 119.8
- [ ] Average Pressure ≈ 6.09
- [ ] Average Temperature ≈ 117.67

---

## 5. Chart Visualization Testing

### Web Application
- [ ] Pie chart displays equipment types
- [ ] Pie chart shows percentages
- [ ] Bar chart shows average parameters
- [ ] Line chart shows trends
- [ ] Charts are responsive
- [ ] Charts update when switching datasets
- [ ] Colors are visually appealing

### Desktop Application
- [ ] Charts tab displays two charts
- [ ] Pie chart shows equipment distribution
- [ ] Bar chart shows parameter averages
- [ ] Charts have proper labels
- [ ] Charts are readable
- [ ] Charts update with dataset change

---

## 6. Dataset History Testing

### Web Application
- [ ] History section shows uploaded datasets
- [ ] Shows up to 5 datasets
- [ ] Each item shows filename and timestamp
- [ ] Each item shows record count
- [ ] Can click to switch datasets
- [ ] Active dataset is highlighted
- [ ] Oldest datasets removed after 5

### Desktop Application
- [ ] Dropdown shows all datasets
- [ ] Can select different datasets
- [ ] Dataset info displayed correctly
- [ ] UI updates on selection change
- [ ] Shows up to 5 datasets

---

## 7. PDF Report Testing

### Web Application
- [ ] Download PDF button visible
- [ ] Clicking button downloads file
- [ ] PDF filename is correct
- [ ] PDF can be opened
- [ ] PDF contains title
- [ ] PDF shows dataset info
- [ ] PDF includes equipment type table
- [ ] PDF includes statistics table
- [ ] PDF includes data table
- [ ] PDF formatting is clean

### Desktop Application
- [ ] Download PDF button visible
- [ ] Click opens save dialog
- [ ] Can specify save location
- [ ] PDF downloads successfully
- [ ] Success message shown
- [ ] PDF content matches web version

---

## 8. Error Handling Testing

### Invalid File Tests
- [ ] Non-CSV file rejected (try .txt, .xlsx)
- [ ] Empty CSV shows error
- [ ] CSV with wrong columns shows error
- [ ] CSV with missing data handled gracefully

### Network Error Tests
- [ ] Stop backend, check web app error messages
- [ ] Stop backend, check desktop app error messages
- [ ] Slow connection handled (mock with throttling)

### Authentication Error Tests
- [ ] Expired session redirects to login
- [ ] Unauthorized access blocked
- [ ] Session persistence works

---

## 9. UI/UX Testing

### Web Application
- [ ] Layout is responsive
- [ ] Mobile view works (resize browser)
- [ ] Colors are consistent
- [ ] Buttons have hover effects
- [ ] Loading states shown
- [ ] Error messages are clear
- [ ] Success messages displayed
- [ ] Gradient backgrounds work
- [ ] Font sizes readable

### Desktop Application
- [ ] Window can be resized
- [ ] All elements visible on resize
- [ ] Tabs work correctly
- [ ] Buttons respond to clicks
- [ ] Text is readable
- [ ] Layout is organized
- [ ] Status bar updates

---

## 10. Performance Testing

### Upload Performance
- [ ] Small CSV (15 rows) uploads quickly
- [ ] Medium CSV (100 rows) uploads successfully
- [ ] Large CSV (1000 rows) uploads (if possible)
- [ ] Upload progress indication

### Data Loading
- [ ] Dataset loads within 2 seconds
- [ ] Charts render quickly
- [ ] Table loads without lag
- [ ] Switching datasets is smooth

### Memory Usage
- [ ] No memory leaks on repeated uploads
- [ ] Application remains responsive
- [ ] Browser doesn't slow down

---

## 11. Data Validation Testing

### Test with Different Data
- [ ] All positive numbers work
- [ ] Decimal numbers handled correctly
- [ ] Large numbers (1000+) work
- [ ] Small numbers (0.1) work
- [ ] Equipment names with spaces work
- [ ] Special characters in names work

### Test Edge Cases
- [ ] Single row CSV
- [ ] 100+ rows CSV
- [ ] All same equipment type
- [ ] All different equipment types
- [ ] Zero values (if applicable)

---

## 12. API Testing

### Using Browser or Postman

#### Auth Endpoints
- [ ] POST /api/auth/register/ (create user)
- [ ] POST /api/auth/login/ (login user)
- [ ] GET /api/auth/user/ (get current user)
- [ ] POST /api/auth/logout/ (logout)

#### Dataset Endpoints
- [ ] GET /api/datasets/ (list datasets)
- [ ] POST /api/datasets/ (upload CSV)
- [ ] GET /api/datasets/1/ (get specific dataset)
- [ ] GET /api/datasets/1/summary/ (get summary)
- [ ] GET /api/datasets/1/pdf/ (download PDF)

---

## 13. Security Testing

### Authentication
- [ ] Cannot access datasets without login
- [ ] Cannot access other users' data
- [ ] Session expires appropriately
- [ ] Password is hashed in database

### File Upload
- [ ] Only CSV files accepted
- [ ] File size limits enforced
- [ ] Malicious file names handled
- [ ] SQL injection prevented

---

## 14. Database Testing

### Check Django Admin
- [ ] Access http://localhost:8000/admin
- [ ] Login with superuser
- [ ] View Datasets table
- [ ] View EquipmentRecord table
- [ ] Data stored correctly
- [ ] Timestamps accurate
- [ ] Foreign keys working

### Cleanup Testing
- [ ] Upload 6 datasets
- [ ] Verify only last 5 kept
- [ ] Oldest deleted automatically
- [ ] No orphaned records

---

## 15. Cross-Browser Testing (Web)

Test on multiple browsers:
- [ ] Chrome
- [ ] Firefox
- [ ] Edge
- [ ] Safari (if available)

Check:
- [ ] Login works
- [ ] Upload works
- [ ] Charts display correctly
- [ ] Tables render properly
- [ ] Download works

---

## 16. Integration Testing

### End-to-End Flow
1. [ ] Register new user
2. [ ] Login
3. [ ] Upload sample CSV
4. [ ] View data table
5. [ ] Check summary stats
6. [ ] View charts
7. [ ] Download PDF
8. [ ] Upload another CSV
9. [ ] Switch between datasets
10. [ ] Logout

### Multi-Client Testing
- [ ] Login on web and desktop simultaneously
- [ ] Upload on web, verify on desktop
- [ ] Upload on desktop, verify on web
- [ ] Both clients show same data

---

## 17. Documentation Testing

- [ ] README.md is clear
- [ ] SETUP_GUIDE.md has all steps
- [ ] QUICKSTART.md is easy to follow
- [ ] PROJECT_SUMMARY.md is comprehensive
- [ ] Code has comments where needed
- [ ] API endpoints documented

---

## 18. Setup Scripts Testing (Windows)

- [ ] setup_backend.bat works
- [ ] setup_frontend_web.bat works
- [ ] setup_frontend_desktop.bat works
- [ ] start_backend.bat starts server
- [ ] start_web.bat starts React app
- [ ] start_desktop.bat launches PyQt5 app

---

## 19. Final Checks

### Code Quality
- [ ] No syntax errors
- [ ] No console errors (browser)
- [ ] No Python errors
- [ ] Proper error handling
- [ ] Clean code structure

### Functionality
- [ ] All required features implemented
- [ ] CSV upload works
- [ ] Data visualization works
- [ ] Summary statistics accurate
- [ ] History management works
- [ ] PDF generation works
- [ ] Authentication works

### User Experience
- [ ] Intuitive interface
- [ ] Clear error messages
- [ ] Fast response times
- [ ] Professional appearance
- [ ] Consistent styling

---

## 20. Deployment Preparation

- [ ] .gitignore configured
- [ ] No sensitive data in code
- [ ] Requirements.txt complete
- [ ] Package.json complete
- [ ] Database migrations included
- [ ] Sample data included
- [ ] Documentation complete

---

## Test Results Summary

**Date**: __________

**Tester**: __________

**Total Tests**: 200+

**Passed**: _____ / _____

**Failed**: _____ / _____

**Issues Found**: __________

**Status**: ☐ Ready for Submission  ☐ Needs Fixes

---

## Known Issues / Notes

```
List any issues discovered during testing:

1. 
2. 
3. 

```

---

## Sign-off

- [ ] All critical tests passed
- [ ] Documentation reviewed
- [ ] Code reviewed
- [ ] Ready for submission

**Signed**: ________________  **Date**: __________

---

## 🎉 Testing Complete!

If all tests pass, the project is ready for deployment and submission!
