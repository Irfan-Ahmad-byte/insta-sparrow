# 🐦 Insta-Sparrow

Automate Instagram outreach — Fetch followers from target accounts and send promotional direct messages (DMs) using Selenium.

## 🚀 Overview

Insta-Sparrow is a Python-based automation tool designed to:

-   📥 **Fetch followers** from specified Instagram accounts.
-   💬 **Send direct messages** to those followers with promotional content.

Built with Selenium WebDriver, this tool simulates human interactions to navigate Instagram's web interface, making it ideal for marketing campaigns and audience engagement.

## 🧠 Features

-   **Competitor Analysis:** Retrieve followers from competitor accounts to target potential customers.
-   **Automated Messaging:** Send personalized DMs to fetched followers.
-   **Docker Support:** Easily deploy and run the application in a containerized environment.
-   **Environment Configuration:** Utilize `.env` files for secure and flexible configuration.

## 🛠️ Tech Stack

-   **Programming Language:** Python
-   **Automation:** Selenium WebDriver
-   **Containerization:** Docker, Docker Compose
-   **Environment Management:** `.env` files

## 📦 Installation

1.  **Clone the Repository**

    ```bash
    git clone [https://github.com/Irfan-Ahmad-byte/insta-sparrow.git](https://github.com/Irfan-Ahmad-byte/insta-sparrow.git)
    cd insta-sparrow
    ```

2.  **Set Up Environment Variables**

    Create a `.env` file in the root directory and configure the following variables:

    ```env
    INSTAGRAM_USERNAME=your_instagram_username
    INSTAGRAM_PASSWORD=your_instagram_password
    TARGET_ACCOUNTS=comma_separated_target_usernames
    MESSAGE=Your promotional message here
    ```

    Refer to the `.env.example` file for guidance.

3.  **Build and Run with Docker Compose**

    ```bash
    docker-compose up --build
    ```

## 🔍 Usage

1.  **Configure Targets**

    Specify the target Instagram usernames in the `TARGET_ACCOUNTS` environment variable.

2.  **Customize Message**

    Define your promotional message in the `MESSAGE` environment variable.

3.  **Run the Application**

    Execute the application to start fetching followers and sending DMs.

## ⚠️ Disclaimer

-   **Compliance:** Ensure that your use of this tool complies with Instagram's terms of service and community guidelines.
-   **Rate Limiting:** Be cautious of Instagram's rate limits to avoid temporary bans or restrictions.
-   **Maintenance:** Instagram's web interface may change over time; updates to the selectors and logic may be necessary.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Developed by [Irfan Ahmad](!https://github.com/irfan-ahmad-byte)