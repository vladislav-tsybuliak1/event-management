CANCEL_REGISTRATION_HTML_CONTENT = """
<html>
<head></head>
<body>
    <div style="border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); padding: 20px; max-width: 400px; margin: 20px auto; font-family: 'Arial', sans-serif; background-color: #f9f9f9;">
        <h2 style="color: #007BFF; text-align: center; margin-top: 0;">Welcome to Event Management!</h2>
        <p style="margin: 10px 0; line-height: 1.5;">Dear {username},</p>
        <p style="margin: 10px 0; line-height: 1.5;">You've successfully canceled the event at <strong>{event}</strong>!</p>
        <br>
        <p style="margin: 10px 0; line-height: 1.5;">Regards,</p>
        <p style="margin: 10px 0; line-height: 1.5; font-style: italic;">The Event Management team</p>
    </div>
</body>
</html>
"""
