# 🧪 OCINT Chat Testing Guide

## 🎯 **How to Test the OCINT Victim Chat**

### **Option 1: Use the Dedicated OCINT Chat Page (Recommended)**

1. **Open the OCINT-specific chat page**:
   ```
   http://localhost:3000/ocint-victim-chat.html
   ```

2. **This page is specifically designed for crypto theft victim reports** and includes:
   - ✅ OCINT branding and styling
   - ✅ Step-by-step conversation flow
   - ✅ Progress tracking
   - ✅ Information extraction
   - ✅ Automatic escalation

### **Option 2: Use the General Customer Chat Page**

1. **Open the general customer chat**:
   ```
   http://localhost:3000/customer-chat.html
   ```

2. **⚠️ Note**: This page is **NOT yet integrated** with the OCINT MVP we built. It's set up for general customer support.

## 🎭 **Test Scenarios - What to Say**

### **Scenario 1: Complete Bitcoin Theft Report**
```
Step 1: "Hi Alex, thanks for helping me out. My name is John Smith and my email is john@example.com. You can call me at 555-123-4567. Someone stole my Bitcoin yesterday and I'm really freaked out about it."

Step 2: "The theft happened on 2024-01-15 around 2:30 PM. I logged into my wallet and saw all my Bitcoin was gone. I think someone hacked my computer or something."

Step 3: "I lost about 2.5 Bitcoin worth around $100,000. The wallet address was 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa and the transaction hash is abc123def456789..."

Step 4: "Yes, I have screenshots of the wallet showing the transactions and some emails from the exchange. I can provide those."
```

### **Scenario 2: Incomplete Ethereum Theft Report**
```
Step 1: "Hello, I was robbed of my Ethereum. My name is Sarah Johnson, email sarah@test.com, phone 555-987-6543."

Step 2: "It happened last week, I think on Tuesday. I'm not sure of the exact time."

Step 3: "I lost some Ethereum, maybe 10 ETH. I don't have the wallet addresses right now."
```

### **Scenario 3: Complex Multi-Crypto Theft**
```
Step 1: "I need to report a major theft. I'm Mike Chen, mike@company.com, 555-456-7890. This is urgent."

Step 2: "The theft occurred on 2024-01-20 at 11:45 PM. I discovered it when I tried to make a transaction and my wallet was empty. I suspect a phishing attack."

Step 3: "I lost Bitcoin, Ethereum, and Litecoin. About 5 BTC, 50 ETH, and 100 LTC. Total value around $500,000. I have multiple wallet addresses and transaction hashes."

Step 4: "I have extensive evidence including screenshots, transaction records, and email communications with the attackers."
```

## 🔍 **What to Look For During Testing**

### **✅ Expected Behavior**

1. **Step-by-Step Flow**:
   - AI guides you through 5 clear steps
   - Each step asks specific questions
   - Progress bar shows completion percentage

2. **Information Extraction**:
   - AI extracts names, emails, phone numbers
   - AI identifies dates, times, crypto types
   - AI captures wallet addresses and transaction hashes

3. **Efficient Process**:
   - Maximum 8 messages per report
   - Quick escalation when complete
   - Clear status updates

4. **Professional Experience**:
   - Empathetic and helpful tone
   - Clear explanations of what's needed
   - Professional escalation process

### **❌ Issues to Watch For**

1. **Information Not Extracted**:
   - Names, emails, or phone numbers not captured
   - Dates or amounts not recognized
   - Wallet addresses not identified

2. **Flow Problems**:
   - Steps not progressing correctly
   - Questions not matching the step
   - Escalation not triggering

3. **UI Issues**:
   - Progress bar not updating
   - Status panel showing wrong information
   - Messages not displaying properly

## 🚀 **Quick Test Commands**

### **Test the OCINT Chat Page**
```bash
# Navigate to the frontend directory
cd app/frontend

# Start a simple HTTP server (if you don't have one running)
python -m http.server 3000

# Open in browser
open http://localhost:3000/ocint-victim-chat.html
```

### **Test the Backend Integration**
```bash
# Navigate to the MCP servers directory
cd app/mcp-servers

# Start the OCINT backend server
python ocint_backend_integration.py

# Test with curl
curl -X POST http://localhost:8000/api/v1/ocint/start-report \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test-001"}'
```

## 📊 **Testing Checklist**

### **Frontend Testing**
- [ ] Page loads correctly
- [ ] Initial welcome message appears
- [ ] Step 1 questions are displayed
- [ ] Progress bar shows 20% (Step 1/5)
- [ ] Status panel shows correct information
- [ ] Input field accepts text
- [ ] Send button works
- [ ] Messages appear in chat
- [ ] Information extraction works
- [ ] Steps progress correctly
- [ ] Escalation triggers at completion
- [ ] Reset button works

### **Backend Testing**
- [ ] Server starts without errors
- [ ] Health check endpoint responds
- [ ] Start report endpoint works
- [ ] Process message endpoint works
- [ ] Report status endpoint works
- [ ] Escalation endpoint works

### **Integration Testing**
- [ ] Frontend can connect to backend
- [ ] Messages are processed correctly
- [ ] Report data is stored properly
- [ ] Escalation works end-to-end

## 🎯 **Current Status**

### **✅ Ready for Testing**
- **OCINT Victim Chat Page**: `ocint-victim-chat.html` - Fully functional
- **Backend Integration**: `ocint_backend_integration.py` - Ready to run
- **MCP Server**: `ocint_mvp_mcp_server.py` - Ready to deploy

### **⚠️ Needs Integration**
- **General Customer Chat**: `customer-chat.html` - Not yet integrated with OCINT MVP
- **Existing Chat Agent**: `chat-agent.js` - Needs OCINT-specific modifications

## 🚀 **Next Steps for Full Integration**

### **1. Integrate OCINT with Existing Chat**
Update `customer-chat.html` to include an OCINT mode or redirect to the dedicated OCINT page.

### **2. Connect Frontend to Backend**
Update the OCINT chat page to use the backend API instead of client-side processing.

### **3. Deploy MCP Server**
Set up the MCP server to handle OCINT requests from the frontend.

## 🎉 **Ready to Test!**

The **OCINT Victim Chat page** (`ocint-victim-chat.html`) is fully functional and ready for testing. Use the test scenarios above to verify the complete victim report creation workflow.

**Start here**: Open `http://localhost:3000/ocint-victim-chat.html` and try the test scenarios! 🚀
