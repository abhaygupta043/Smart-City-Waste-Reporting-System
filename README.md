# Smart City Waste Reporting System

A web-based platform designed to empower citizens to keep their city clean by reporting waste management issues. Users can submit reports with video evidence, track the status of their reports, and earn reward points for their contributions.

## Features

- **User Authentication**: Secure sign-up and login with email and OTP verification.
- **Waste Reporting**: Submit detailed reports including location, description, and video evidence of waste.
- **Report Tracking**: Monitor the status of submitted reports (Pending, Approved, Rejected).
- **Reward System**: Earn points for every approved report, encouraging active participation.
- **Admin Dashboard**: (Implied) Administrators can review, approve, or reject reports.

## Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite (Default)
- **Frontend**: HTML, CSS, JavaScript (Django Templates)

## Installation

Follow these steps to set up the project locally:

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd managementAccountability
    ```

2.  **Create a Virtual Environment**
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Database Migrations**
    Initialize the database setup.
    ```bash
    python manage.py migrate
    ```

5.  **Run the Development Server**
    ```bash
    python manage.py runserver
    ```
    Access the application at `http://127.0.0.1:8000/`.

## Configuration

### Email Setup (Required for OTP & Password Reset)
To enable email-based features, you need to configure your email credentials in the settings.

1.  Open the settings file: [waste_management/settings.py](cci:7://file:///c:/Users/abhis/OneDrive/Desktop/managementAccountability%20%283%29/managementAccountability/waste_management/settings.py:0:0-0:0).
2.  Scroll to the bottom to find the email configuration section.
3.  Update the following variables with your actual Gmail credentials:

    ```python
    EMAIL_HOST_USER = 'your-email@gmail.com'
    EMAIL_HOST_PASSWORD = 'your-app-password'
    ```

    > **Important:** Do not use your regular Gmail password. You must generate an **App Password**:
    > 1. Go to your [Google Account Settings](https://myaccount.google.com/security).
    > 2. Enable **2-Step Verification**.
    > 3. Search for **App Passwords** and create one.
    > 4. Use that 16-character code as your `EMAIL_HOST_PASSWORD`.

## Usage

1.  **Register/Login**: Create an account using your email.
2.  **Submit a Report**: Navigate to the reporting section, upload a video, provide details, and submit.
3.  **Track Status**: Check your dashboard to see updates on your reports.
4.  **Earn Points**: Watch your reward points grow as your reports are validated.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements.
