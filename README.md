# StructNova Africa

**A Professional Structural Engineering Web Application**

Built by Aliyu Bashir Nasir - Future Structural Engineer & Engineering Software Developer

---

## 🏗️ About

StructNova Africa is a comprehensive web application that showcases structural engineering expertise while providing professional engineering calculation tools. The platform combines modern web technologies with structural engineering principles to deliver an intuitive, professional experience.

### Key Features

- **Professional Portfolio**: Showcase engineering background, vision, and mission
- **One-Way Slab Calculator**: Complete structural design calculator based on BS 8110 and Eurocode 2
- **Responsive Design**: Fully responsive layout for desktop, tablet, and mobile devices
- **Modern UI/UX**: Clean, professional interface with engineering-themed design

---

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Templating**: Jinja2
- **Styling**: Custom CSS with CSS Variables
- **Icons**: Font Awesome
- **Deployment**: Render (Gunicorn)

---

## 📁 Project Structure

```
structnova-africa/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── Procfile               # Render deployment configuration
├── runtime.txt            # Python version specification
├── README.md              # Project documentation
│
├── templates/             # HTML templates
│   ├── base.html          # Base template with navigation and footer
│   ├── index.html         # Home page
│   ├── about.html         # About page
│   ├── vision.html        # Vision & Mission page
│   └── calculator.html    # One-Way Slab Calculator
│
└── static/                # Static assets
    ├── css/
    │   └── style.css      # Main stylesheet
    └── images/
        └── aliyu.jpg      # Profile image
```

---

## 🚀 Deployment Instructions

### Deploy to Render

1. **Create a Render Account**
   - Go to [render.com](https://render.com) and sign up

2. **Create a New Web Service**
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository or upload the code

3. **Configure the Service**
   - **Name**: `structnova-africa` (or your preferred name)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (or paid for production)

4. **Environment Variables** (Optional)
   - `SECRET_KEY`: A secure random string for session management
   - `FLASK_DEBUG`: Set to `False` for production

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy your application

### Local Development

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd structnova-africa
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the Application**
   - Open your browser and go to `http://localhost:5000`

---

## 🧮 One-Way Slab Calculator

The calculator performs comprehensive structural analysis including:

### Input Parameters
- **Span (L)**: Length of the slab in meters
- **Dead Load (G)**: Permanent loads in kN/m²
- **Live Load (Q)**: Variable loads in kN/m²
- **Concrete Grade**: C20, C25, C30, C35, C40
- **Steel Grade**: 460 MPa or 500 MPa
- **Cover**: Concrete cover to reinforcement in mm

### Calculations
1. **Load Combination**: BS 8110 (1.4G + 1.6Q)
2. **Maximum Bending Moment**: wL²/8 for simply supported slabs
3. **Effective Depth**: d = h - cover - Ø/2
4. **Moment Resistance Factor**: K = M/(bd²fck)
5. **Lever Arm**: z = d[0.5 + √(0.25 - K/1.134)]
6. **Required Steel Area**: As = M/(0.87fy·z)
7. **Minimum Reinforcement**: As,min = 0.0013·b·h
8. **Reinforcement Selection**: Bar size and spacing
9. **Deflection Check**: Span/depth ratio verification
10. **Shear Check**: Concrete shear capacity verification

### Output
- Complete step-by-step calculations
- Reinforcement suggestions with alternatives
- Design verification checks
- Professional summary box

---

## 🎨 Design Standards

The application adheres to:

- **BS 8110-1:1997**: British Standard for structural use of concrete
- **Eurocode 2 (EN 1992-1-1)**: Design of concrete structures
- **Responsive Web Design**: Mobile-first approach

---

## 👤 Owner Information

**Name**: Aliyu Bashir Nasir  
**Title**: Future Structural Engineer & Engineering Software Developer  
**Location**: Nigeria  
**Email**: aliyu.bashir@structnova.africa  
**LinkedIn**: [linkedin.com/in/aliyubashirnasir](https://linkedin.com/in/aliyubashirnasir)

---

## 📄 License

© 2026 Aliyu Bashir Nasir. All rights reserved.

---

## 🤝 Contributing

This is a personal portfolio project. For suggestions or feedback, please contact via email.

---

## 🙏 Acknowledgments

- BS 8110 and Eurocode 2 standards for structural design principles
- Flask community for the excellent web framework
- Render for free hosting services
