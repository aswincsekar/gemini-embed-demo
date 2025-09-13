"""
Example usage of the SmartHelpCenter with sample data.
This script demonstrates how to use the help center for a typical SaaS application.
"""

import os
from help_center import SmartHelpCenter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    """Run the help center example."""
    
    # Initialize the help center
    print("🚀 Initializing Smart Help Center...")
    help_center = SmartHelpCenter(collection_name="saas_help_articles")
    
    # Clear any existing articles for a fresh start
    help_center.clear_all_articles()
    
    # Sample help articles for a SaaS application
    sample_articles = [
        {
            "article_id": "pwd-001",
            "title": "How to Reset Your Password",
            "content": """If you've forgotten your password, don't worry! Here's how to reset it:

1. Click on 'Forgot Password' on the login page
2. Enter your email address associated with your account
3. Check your email inbox for a password reset link (check spam folder too)
4. Click the reset link within 24 hours (links expire for security)
5. Create a new password that meets our requirements:
   - At least 8 characters long
   - Contains at least one uppercase letter
   - Contains at least one number
   - Contains at least one special character (!@#$%^&*)
6. Click 'Save New Password'

If you don't receive the reset email within 5 minutes, try:
- Checking your spam/junk folder
- Adding noreply@ourapp.com to your contacts
- Requesting a new reset link""",
            "category": "account"
        },
        {
            "article_id": "pwd-002",
            "title": "Password Security Best Practices",
            "content": """Keep your account secure with these password tips:

- Use a unique password for our platform
- Enable two-factor authentication (2FA) in Security Settings
- Never share your password with anyone
- Change your password every 90 days
- Use a password manager to generate and store strong passwords
- Avoid using personal information in passwords
- Don't use the same password across multiple sites""",
            "category": "account"
        },
        {
            "article_id": "bill-001",
            "title": "Understanding Your Billing and Payments",
            "content": """Your subscription billing works as follows:

**Billing Cycle:**
- Subscriptions are billed monthly on the same date you signed up
- Annual plans are billed once per year with a 20% discount
- You can switch between monthly and annual billing anytime

**Payment Methods:**
- Credit/Debit cards (Visa, Mastercard, Amex)
- PayPal
- Wire transfer (Enterprise plans only)

**Managing Payments:**
1. Go to Settings > Billing
2. View your current plan and usage
3. Update payment method
4. Download invoices (PDF format)
5. View payment history

**Failed Payments:**
- We'll retry failed payments up to 3 times over 7 days
- You'll receive email notifications about payment issues
- Your account remains active during the retry period
- After 7 days, accounts may be suspended (data is preserved)""",
            "category": "billing"
        },
        {
            "article_id": "bill-002",
            "title": "Upgrading or Downgrading Your Plan",
            "content": """You can change your subscription plan at any time:

**To Upgrade:**
1. Go to Settings > Billing > Change Plan
2. Select your new plan
3. Review the prorated charges
4. Confirm the upgrade
5. New features are available immediately

**To Downgrade:**
1. Go to Settings > Billing > Change Plan
2. Select a lower tier
3. Review what features you'll lose
4. Confirm the downgrade
5. Changes take effect at the next billing cycle

**Important Notes:**
- Upgrades are prorated and charged immediately
- Downgrades take effect at the start of your next billing period
- Unused credits from upgrades are applied to future invoices
- Some features may be limited when downgrading""",
            "category": "billing"
        },
        {
            "article_id": "exp-001",
            "title": "Exporting Your Data",
            "content": """Export your data in multiple formats for analysis or backup:

**Available Export Formats:**
- CSV (Excel compatible)
- JSON (for developers)
- PDF (formatted reports)
- XML (legacy systems)

**How to Export:**
1. Navigate to the data you want to export
2. Click the Export button (⬇️ icon) in the top-right corner
3. Choose your format
4. Select date range (last 30 days, custom range, all time)
5. Choose specific fields to include/exclude
6. Click 'Generate Export'

**Large Exports:**
- Exports over 10,000 records are processed in the background
- You'll receive an email with a download link when ready
- Links expire after 7 days for security
- Maximum export size is 5GB

**Scheduling Exports:**
Premium users can schedule automatic exports:
1. Go to Settings > Automation > Scheduled Exports
2. Set frequency (daily, weekly, monthly)
3. Choose format and destination (email, FTP, cloud storage)""",
            "category": "features"
        },
        {
            "article_id": "api-001",
            "title": "Getting Started with Our API",
            "content": """Our RESTful API allows you to integrate our service with your applications:

**API Access:**
1. Go to Settings > API Keys
2. Click 'Generate New API Key'
3. Copy your key immediately (it won't be shown again)
4. Add the key to your request headers: `Authorization: Bearer YOUR_API_KEY`

**Rate Limits:**
- Free tier: 100 requests per hour
- Pro tier: 1,000 requests per hour
- Enterprise: Unlimited

**Base URL:** `https://api.ourapp.com/v2/`

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.ourapp.com/v2/data
```

**Common Endpoints:**
- GET /data - Retrieve your data
- POST /data - Create new records
- PUT /data/{id} - Update existing records
- DELETE /data/{id} - Delete records

Full API documentation: https://docs.ourapp.com/api""",
            "category": "developers"
        },
        {
            "article_id": "int-001",
            "title": "Integrations and Webhooks",
            "content": """Connect our platform with your favorite tools:

**Available Integrations:**
- Slack: Get notifications in your channels
- Zapier: Connect with 3000+ apps
- Google Sheets: Sync data automatically
- Salesforce: Bi-directional sync
- Microsoft Teams: Notifications and updates

**Setting Up Webhooks:**
1. Go to Settings > Integrations > Webhooks
2. Click 'Add Webhook'
3. Enter your endpoint URL
4. Select events to trigger the webhook
5. Add optional headers for authentication
6. Test the webhook with sample data
7. Save and activate

**Webhook Events:**
- record.created
- record.updated
- record.deleted
- user.login
- payment.success
- payment.failed

**Webhook Security:**
- All webhooks include an HMAC signature
- Verify signatures to ensure requests are from us
- Retry logic: 3 attempts with exponential backoff
- View webhook logs in Settings > Integrations > Logs""",
            "category": "developers"
        },
        {
            "article_id": "team-001",
            "title": "Managing Team Members",
            "content": """Collaborate effectively with team management features:

**Adding Team Members:**
1. Go to Settings > Team
2. Click 'Invite Team Member'
3. Enter their email address
4. Select their role (Admin, Editor, Viewer)
5. Choose which projects they can access
6. Send invitation

**User Roles:**
- **Admin**: Full access, can manage billing and users
- **Editor**: Can create, edit, and delete data
- **Viewer**: Read-only access

**Managing Permissions:**
- Set project-level permissions
- Create custom roles (Enterprise only)
- Enable/disable specific features per user
- Set up approval workflows

**Removing Users:**
1. Go to Settings > Team
2. Click the ⋮ menu next to the user
3. Select 'Remove from team'
4. Choose whether to transfer their data
5. Confirm removal""",
            "category": "collaboration"
        },
        {
            "article_id": "sec-001",
            "title": "Security and Compliance",
            "content": """We take your data security seriously:

**Security Features:**
- 256-bit AES encryption at rest
- TLS 1.3 encryption in transit
- SOC 2 Type II certified
- GDPR and CCPA compliant
- Regular third-party security audits

**Two-Factor Authentication (2FA):**
1. Go to Settings > Security
2. Click 'Enable 2FA'
3. Scan QR code with authenticator app
4. Enter verification code
5. Save backup codes securely

**Session Management:**
- Sessions expire after 24 hours of inactivity
- View active sessions in Settings > Security
- Revoke sessions from unrecognized devices

**Data Protection:**
- Daily automated backups
- Point-in-time recovery (last 30 days)
- Data residency options (US, EU, APAC)
- Right to deletion (GDPR Article 17)

**Compliance Documents:**
Download our compliance certificates and policies from Settings > Compliance""",
            "category": "security"
        }
    ]
    
    # Index the articles
    print("\n📚 Indexing help articles...")
    help_center.index_help_articles(sample_articles)
    
    # Show statistics
    stats = help_center.get_statistics()
    print(f"\n📊 Help Center Statistics:")
    print(f"   Total articles: {stats['total_articles']}")
    print(f"   Categories: {stats['categories']}")
    print(f"   Avg article length: {stats['avg_article_length']:.0f} characters")
    
    # Test with various user queries
    test_queries = [
        ("I forgot my password", None),
        ("can't login to my account", None),
        ("how much does this cost", "billing"),
        ("export to excel", None),
        ("payment failed help", None),
        ("how to add team members", "collaboration"),
        ("is my data secure", "security"),
        ("API rate limits", "developers"),
        ("cancel subscription", "billing"),
        ("webhook not working", "developers")
    ]
    
    print("\n🔍 Testing user queries:\n")
    print("=" * 80)
    
    for query, category in test_queries:
        print(f"\n📝 User Query: '{query}'")
        if category:
            print(f"   Category Filter: {category}")
        
        result = help_center.answer_support_query(
            query, 
            top_k=3,
            category_filter=category
        )
        
        print(f"\n🤖 Answer:")
        print(f"   {result['answer'][:300]}...")
        
        print(f"\n📊 Confidence: {result['confidence']}")
        
        print(f"\n📚 Related Articles:")
        for article in result['relevant_articles']:
            print(f"   - {article['title']} (Score: {article['relevance_score']:.2f})")
        
        print("\n" + "-" * 80)
    
    # Example of chunking a long article
    print("\n🔧 Example of Smart Chunking:")
    long_article = """
    ## Introduction to Our Platform
    
    Welcome to our comprehensive platform that helps you manage your business efficiently.
    This guide will walk you through all the features and capabilities.
    
    ## Getting Started
    
    First, you'll need to create an account. Visit our website and click on the Sign Up button.
    Fill in your details including email, password, and company information.
    After verification, you'll have access to your dashboard.
    
    The dashboard is your central hub where you can see all your important metrics at a glance.
    You can customize widgets, set up alerts, and access all features from here.
    
    ## Advanced Features
    
    Our platform includes advanced analytics that help you make data-driven decisions.
    You can create custom reports, set up automated workflows, and integrate with third-party tools.
    
    The API allows developers to build custom integrations and extend functionality.
    We provide comprehensive documentation and SDKs in multiple programming languages.
    """
    
    from help_center import smart_chunk
    chunks = smart_chunk(long_article, max_tokens=100)
    print(f"Article split into {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"\nChunk {i} ({len(chunk)} chars):")
        print(f"   {chunk[:100]}...")
    
    print("\n✅ Example completed successfully!")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY not found in environment variables.")
        print("   Please create a .env file with your API key:")
        print("   GEMINI_API_KEY=your_api_key_here")
    else:
        main()
