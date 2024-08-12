import streamlit as st
from PIL import Image
import folium
from streamlit_folium import st_folium
from datetime import date
import stripe
import smtplib
from email.mime.text import MIMEText
from folium.plugins import MarkerCluster
import base64
import io
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="Agadir Golden Trip", page_icon="⚓", layout="wide")

# Load and encode logo
logo_image_path = "/Users/yassine/Downloads/Untitled design-2.png"  # Update the path as necessary
logo_image = Image.open(logo_image_path)

# Convert logo to bytes and then to base64
buffered_logo = BytesIO()
logo_image.save(buffered_logo, format="PNG")
logo_base64 = base64.b64encode(buffered_logo.getvalue()).decode()

# Load and encode background image
background_image_path = "/Users/yassine/Downloads/92686376_m_normal_none.jpg"  # Update the path as necessary
background_image = Image.open(background_image_path)

# Convert background to bytes and then to base64
buffered_bg = BytesIO()
background_image.save(buffered_bg, format="JPEG")
background_base64 = base64.b64encode(buffered_bg.getvalue()).decode()

# Include Bootstrap CSS and custom styles
st.markdown(f"""
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;700&family=Lora:wght@400;700&display=swap');
        
        body {{
            margin: 0;
            font-family: 'Lora', serif;
            background-color: #f5f5f5;
        }}
        .navbar-custom {{
            background-color: rgba(0, 47, 108, 0.85);
            backdrop-filter: blur(10px);
            padding: 10px 20px;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1030;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            border-bottom: 1px solid #ffd700; /* Gold border */
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .navbar-nav {{
            font-size: 1em;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            display: flex;
            align-items: center;
        }}
        .navbar-nav .nav-link {{
            color: #ffd700 !important;
            margin: 0 10px;
            padding: 8px 12px;
            border-radius: 20px;
            font-weight: 500;
            transition: color 0.3s ease-in-out, background-color 0.3s ease-in-out;
            position: relative;
        }}
        .navbar-nav .nav-link:hover {{
            color: #ffffff !important;
            background-color: rgba(255, 215, 0, 0.2);
        }}
        .navbar-nav .nav-link:before {{
            content: '';
            display: block;
            position: absolute;
            bottom: -5px;
            left: 50%;
            width: 0;
            height: 2px;
            background-color: #ffd700;
            transition: width 0.3s ease, left 0.3s ease;
        }}
        .navbar-nav .nav-link:hover:before {{
            width: 100%;
            left: 0;
        }}
        .dropdown-menu {{
            background-color: rgba(0, 47, 108, 0.95);
            border: 1px solid #ffd700;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        .dropdown-item {{
            color: #ffd700 !important;
            font-weight: 500;
        }}
        .dropdown-item:hover {{
            background-color: rgba(255, 215, 0, 0.3);
            color: #fff !important;
        }}
        .hero-section {{
            background: linear-gradient(to right, rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                        url('data:image/jpeg;base64,{background_base64}') no-repeat center center;
            background-size: cover;
            color: #fff;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 0 20px;
            position: relative;
        }}
        .hero-title {{
            font-size: 4em;
            font-weight: 700;
            font-family: 'Cormorant Garamond', serif;
            color: #ffd700;
            animation: slideIn 1.5s ease-in-out;
        }}
        .hero-subtitle {{
            font-size: 1.4em;
            color: #e0e0e0;
            animation: slideIn 2s ease-in-out;
        }}
        .hero-buttons {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }}
        .hero-button-primary {{
            font-size: 1.2em;
            padding: 12px 30px;
            border-radius: 30px;
            border: none;
            text-decoration: none;
            background: linear-gradient(135deg, #ff7e5f, #feb47b);
            color: #fff;
            font-weight: 600;
            transition: background 0.3s, transform 0.3s;
        }}
        .hero-button-primary:hover {{
            background: linear-gradient(135deg, #feb47b, #ff7e5f);
            transform: translateY(-4px);
        }}
        @keyframes slideIn {{
            from {{
                transform: translateY(-50px);
                opacity: 0;
            }}
            to {{
                transform: translateY(0);
                opacity: 1;
            }}
        }}
        .footer {{
            background-color: #002b5e;
            color: #fff;
            padding: 20px;
            text-align: center;
            box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.3);
        }}
        .footer a {{
            color: #ffd700;
            text-decoration: none;
            font-weight: 500;
        }}
        .footer a:hover {{
            text-decoration: underline;
        }}
        .social-icons {{
            margin-top: 10px;
        }}
        .social-icons a {{
            color: #ffd700;
            margin: 0 10px;
            font-size: 1.5em;
            transition: color 0.3s;
        }}
        .social-icons a:hover {{
            color: #fff;
        }}
        .logo-container {{
            position: absolute;
            top: 15px;
            right: 20px;
            background: rgba(255, 215, 0, 0.8);
            border-radius: 50%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            padding: 5px;
        }}
        .logo-img {{
            height: 60px;
            border: 2px solid #ffd700;
            background-color: #002f6c;
            border-radius: 50%;
        }}
    </style>
""", unsafe_allow_html=True)

# Navbar
st.markdown(f"""
    <nav class="navbar navbar-expand-lg navbar-custom">
        <div class="container-fluid">
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Experiences</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Luxury Cruises</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Private Tours</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Exclusive Packages</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
""", unsafe_allow_html=True)

# Hero Section
st.markdown(f"""
    <section class="hero-section">
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" alt="Logo" class="logo-img">
        </div>
        <div class="hero-content">
            <h1 class="hero-title">Welcome to <span class="highlight">Agadir Golden Trip</span></h1>
            <p class="hero-subtitle">Experience luxury like never before.</p>
            <div class="hero-buttons">
                <a href="#" class="hero-button-primary">Discover More</a>
                <a href="#" class="hero-button-primary">Book Now</a>
            </div>
        </div>
    </section>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <footer class="footer">
        <p>&copy; 2024 Agadir Golden Trip. All rights reserved.</p>
        <div class="social-icons">
            <a href="#" class="fa fa-facebook"></a>
            <a href="#" class="fa fa-twitter"></a>
            <a href="#" class="fa fa-instagram"></a>
        </div>
    </footer>
""", unsafe_allow_html=True)




# ---- WHAT WE DO ----
with st.container():
    st.write("---")  # Line separator

    # Add a bit of spacing
    st.write("##")

    # Display the "What We Do" section with a more polished design
    st.markdown("""
    <section class="what-we-do">
        <h2 class="section-title">Our Services</h2>
        <div class="services-container">
            <div class="service">
                <h3>Luxurious Boat Rentals</h3>
                <p>Enjoy the best-in-class boats for your sea adventures. Our fleet is equipped with top-of-the-line amenities for a memorable experience.</p>
            </div>
            <div class="service">
                <h3>Custom Sailing Experiences</h3>
                <p>Tailored experiences to suit your needs. Whether you're planning a romantic getaway or a family outing, we customize each trip to your preference.</p>
            </div>
            <div class="service">
                <h3>Expert Support</h3>
                <p>Our team ensures a safe and enjoyable trip. From booking to sailing, we provide expert assistance every step of the way.</p>
            </div>
            <div class="service">
                <h3>Flexible Packages</h3>
                <p>Choose from a variety of packages or customize your own. We offer options to fit every budget and occasion.</p>
            </div>
        </div>
    </section>
    """, unsafe_allow_html=True)

# Styling for the "What We Do" section
st.markdown("""
<style>
    .what-we-do {
        background-color: #f8f9fa;
        padding: 40px 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 20px auto;
        max-width: 1200px;
    }
    .section-title {
        font-size: 2.5em;
        color: #002f6c; /* Dark blue color */
        text-align: center;
        font-family: 'Cormorant Garamond', serif;
        margin-bottom: 20px;
    }
    .services-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
    }
    .service {
        background: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        flex: 1 1 45%;
        max-width: 45%;
        text-align: center;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .service h3 {
        color: #002f6c; /* Dark blue color */
        font-size: 1.5em;
        margin-bottom: 10px;
    }
    .service p {
        color: #333;
        font-size: 1em;
    }
    .service:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)


# ---- PROGRAM ----
with st.container():
    st.write("---")
    st.header("Discover Our Exclusive Programs")
    st.write("##")
    
    st.markdown("""
        <div style="text-align: center;">
            <h2 style="color: #FFD700; font-family: 'Cormorant Garamond', serif; font-weight: 700;">Morning Journey (9 AM - 2 PM)</h2>
            <div style="background: rgba(0, 47, 108, 0.9); padding: 20px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); color: #f5f5f5;">
                <p style="font-size: 1.2em; line-height: 1.8;">
                    <strong>Start your day with an exclusive experience:</strong><br>
                    <ul style="list-style-type: none; padding: 0;">
                        <li><strong>&#9733; Refreshing Fishing Experience:</strong> Cast your line and enjoy the thrill of fishing in pristine waters.</li>
                        <li><strong>&#9733; Invigorating Swim:</strong> Dive into crystal-clear waters for a refreshing swim.</li>
                        <li><strong>&#9733; Gourmet Barbecue Lunch:</strong> Relish a delicious, freshly prepared barbecue meal onboard.</li>
                        <li><strong>&#9733; Joyful Moments with Our Crew:</strong> Enjoy the company of our friendly and professional crew for a memorable day.</li>
                    </ul>
                </p>
            </div>
            <br>
            <h2 style="color: #FFD700; font-family: 'Cormorant Garamond', serif; font-weight: 700;">Afternoon Boat Rental (2 PM - 7 PM)</h2>
            <div style="background: rgba(0, 47, 108, 0.9); padding: 20px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); color: #f5f5f5;">
                <p style="font-size: 1.2em; line-height: 1.8;">
                    <strong>Exclusive Boat Rental Options:</strong><br>
                    - <strong>Boat Rental:</strong> From 300 USD per hour.<br>
                    - <strong>Additional Excitement:</strong> Customize your adventure with our premium additions:
                    <ul style="list-style-type: none; padding: 0;">
                        <li><strong>&#9733; Food:</strong> Choose from a variety of gourmet options.</li>
                        <li><strong>&#9733; Jet Ski:</strong> Add some thrill to your ride.</li>
                        <li><strong>&#9733; Flyboard:</strong> Soar above the water with our flyboard experience.</li>
                        <li><strong>&#9733; Diving:</strong> Discover the underwater world with guided diving.</li>
                    </ul>
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

#Gallery 

import streamlit as st
from PIL import Image
import base64
import io

# Function to convert image to base64
def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# Load custom CSS for styling
def load_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;600&display=swap');

        body {
            font-family: 'Open Sans', sans-serif;
        }

        .catalogue-title {
            font-family: 'Playfair Display', serif;
            font-size: 3em;
            color: #FFD700;
            text-align: center;
            margin-bottom: 40px;
        }

        .catalogue-container {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            gap: 20px;
            padding: 20px;
            background-color: #282828;
            border-radius: 20px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
            width: 100%;
            max-width: 800px;
            cursor: pointer;
            position: relative;
        }

        .catalogue-cover {
            width: 100%;
            height: 500px;
            border: 5px solid #FFD700;
            border-radius: 15px;
            background: url('PLACEHOLDER') no-repeat center center;
            background-size: cover;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }

        .catalogue-cover .button {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            padding: 15px 30px;
            background-color: #FFD700;
            color: #282828;
            font-family: 'Open Sans', sans-serif;
            font-size: 1.2em;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .catalogue-cover .button:hover {
            background-color: #e5c400;
        }

        .full-gallery {
            display: none;
            flex-wrap: wrap;
            gap: 20px;
            padding-top: 20px;
            opacity: 0;
            transition: opacity 0.5s ease;
        }

        .full-gallery.show {
            display: flex;
            opacity: 1;
        }

        .swiper-container {
            width: 100%;
            height: 100%;
        }

        .swiper-slide img {
            width: 100%;
            height: auto;
            border-radius: 15px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Load custom CSS
load_css()

# Title of the catalogue
st.markdown('<div class="catalogue-title">Our Luxurious Trips</div>', unsafe_allow_html=True)

# Define image paths
cover_image_path = "/Users/yassine/Downloads/Moment-5.png"
gallery_image_paths = [
    "/Users/yassine/Downloads/WhatsApp Image 2024-06-26 at 12.53.14 (4).jpeg",
    "/Users/yassine/Downloads/WhatsApp Image 2024-06-28 at 17.00.46 (1).jpeg",
    "/Users/yassine/Downloads/WhatsApp Image 2024-06-26 at 12.53.14 (3).jpeg",
    "/Users/yassine/Downloads/WhatsApp Image 2024-06-28 at 18.11.57.jpeg",
    "/Users/yassine/Downloads/WhatsApp Image 2024-07-01 at 17.36.32.jpeg",
]

# Catalogue container with cover image
with st.container():
    cover_img_url = f"url({cover_image_path})"
    st.markdown(f"""
        <div class="catalogue-container">
            <div class="catalogue-cover" style="background-image: {cover_img_url};">
                <button class="button" id="toggle-gallery">View Gallery</button>
            </div>
            <div class="full-gallery" id="gallery">
                <div class="swiper-container">
                    <div class="swiper-wrapper">
    """, unsafe_allow_html=True)

    # Display full gallery with swipe functionality
    for img_path in gallery_image_paths:
        img = Image.open(img_path)
        img_base64 = image_to_base64(img)
        st.markdown(f"""
            <div class="swiper-slide">
                <img src="data:image/jpeg;base64,{img_base64}" alt="Gallery Image">
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div></div></div>', unsafe_allow_html=True)

# Include Swiper.js for swipe functionality
st.markdown("""
    <script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            var swiper = new Swiper('.swiper-container', {
                loop: true,
                pagination: {
                    el: '.swiper-pagination',
                    clickable: true,
                },
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
            });
            
            document.getElementById('toggle-gallery').addEventListener('click', function () {
                var gallery = document.getElementById('gallery');
                if (gallery.classList.contains('show')) {
                    gallery.classList.remove('show');
                } else {
                    gallery.classList.add('show');
                }
            });
        });
    </script>
""", unsafe_allow_html=True)




def local_css():
    st.markdown(
        """
        <style>
        .testimonial-section {
            background-color: #ffffff; /* Clean white background */
            padding: 60px 20px;
            border-radius: 25px;
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
            margin-top: 40px;
        }
        .testimonial-card {
            background-color: #f9f9f9; /* Light grey background for cards */
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
            display: flex;
            align-items: center;
            gap: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #e0e0e0; /* Light border for a clean look */
        }
        .testimonial-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
        }
        .testimonial-photo {
            border-radius: 50%;
            width: 90px;
            height: 90px;
            border: 5px solid #ffd700; /* Luxurious gold border */
            object-fit: cover;
        }
        .testimonial-name {
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        .testimonial-text {
            font-size: 1em;
            color: #666;
            line-height: 1.6;
            margin-top: 10px;
        }
        .rating {
            font-size: 1.2em;
            color: #f39c12;
            margin-bottom: 10px;
        }
        .testimonial-container {
            display: flex;
            flex-wrap: wrap;
            gap: 30px;
            justify-content: center;
        }
        .testimonial-header {
            text-align: center;
            margin-bottom: 40px;
            color: #333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

with st.container():
    st.write("---")
    st.markdown('<div class="testimonial-header">', unsafe_allow_html=True)
    st.header("What Our Customers Say")
    st.write("##")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Load local CSS
    local_css()
    
    # Define testimonials with placeholder images
    testimonials = [
        {"name": "John Doe", "testimonial": "An unforgettable experience! The crew was fantastic, and the scenery was breathtaking.", "rating": 5, "photo": "https://via.placeholder.com/90?text=John+Doe"},
        {"name": "Jane Smith", "testimonial": "The best boat rental service in Agadir! Highly recommended.", "rating": 4, "photo": "https://via.placeholder.com/90?text=Jane+Smith"},
        {"name": "Alice Johnson", "testimonial": "We had an amazing time. The boat was luxurious, and the trip was well-organized.", "rating": 5, "photo": "https://via.placeholder.com/90?text=Alice+Johnson"},
        {"name": "Michael Brown", "testimonial": "A truly luxurious experience. The boat was immaculate, and the service was top-notch.", "rating": 5, "photo": "https://via.placeholder.com/90?text=Michael+Brown"},
        {"name": "Emily Davis", "testimonial": "Perfect day out on the water. Great value for money and excellent customer service.", "rating": 4, "photo": "https://via.placeholder.com/90?text=Emily+Davis"},
        {"name": "Chris Wilson", "testimonial": "Highly recommend! The boat was beautiful, and the crew went above and beyond.", "rating": 5, "photo": "https://via.placeholder.com/90?text=Chris+Wilson"}
    ]
    
    st.markdown('<div class="testimonial-container">', unsafe_allow_html=True)
    
    for testimonial in testimonials:
        # Create a container for each testimonial
        st.markdown(f"""
            <div class="testimonial-card">
                <img src="{testimonial['photo']}" class="testimonial-photo">
                <div>
                    <div class="testimonial-name">{testimonial['name']}</div>
                    <div class="rating">
                        {'⭐' * testimonial['rating'] + '☆' * (5 - testimonial['rating'])}
                    </div>
                    <div class="testimonial-text">{testimonial['testimonial']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


# Stripe and Email Setup
stripe.api_key = "your_stripe_secret_key"

SMTP_SERVER = "smtp.your_email_provider.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        st.write(f"Error sending email: {e}")

def local_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Playfair+Display:wght@700&display=swap');

        body {
            font-family: 'Lato', sans-serif;
            background-color: #f5f5f5;
        }

        .booking-container {
            background: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), 
                        url('your-background-image-url.jpg') no-repeat center center;
            background-size: cover;
            padding: 50px;
            border-radius: 25px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
            margin-top: 40px;
            display: none; /* Initially hidden */
        }
        .booking-header h1 {
            font-family: 'Playfair Display', serif;
            font-size: 2.5em;
            color: #2c3e50;
        }
        .form-section {
            margin-bottom: 25px;
        }
        .form-section label {
            font-weight: bold;
            color: #34495e;
            font-size: 1.1em;
        }
        .form-section input, .form-section select, .form-section textarea {
            width: 100%;
            padding: 12px;
            border-radius: 10px;
            border: 1px solid #bdc3c7;
            margin-top: 8px;
            font-size: 1em;
        }
        .button-submit {
            background: linear-gradient(45deg, #ffd700, #e5b700);
            color: white;
            border: none;
            padding: 16px 24px;
            border-radius: 12px;
            font-size: 1.2em;
            cursor: pointer;
            transition: background 0.4s ease;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }
        .button-submit:hover {
            background: linear-gradient(45deg, #e5b700, #ffd700);
        }
        .monetary-value {
            color: red;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Initialize session state for showing the form
if 'show_form' not in st.session_state:
    st.session_state['show_form'] = False

# Main page content
st.header("Welcome to Agadir Golden Trip")
st.write(
    """
    Explore the beauty of the sea with our luxury yacht experiences. Whether you're looking for a daily journey or an hourly rental, we have the perfect options for you.
    """
)

if st.button("Book Your Trip"):
    st.session_state['show_form'] = True

if st.session_state['show_form']:
    # Load local CSS
    local_css()

    # Show booking form
    st.markdown(
        """
        <script>
        document.querySelector('.booking-container').style.display = 'block';
        </script>
        """,
        unsafe_allow_html=True
    )

    # Booking form container
    st.markdown('<div class="booking-container">', unsafe_allow_html=True)
    st.markdown('<div class="booking-header">', unsafe_allow_html=True)
    st.header("Ready to Set Sail?")
    st.write("##")
    st.write(
        """
        Fill in the form below to book your trip with Agadir Golden Trip. Our team will get back to you shortly to confirm your booking and provide further details.

        Please note that an advance payment is required to reserve your boat.
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Booking Form
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    trip_date = st.date_input("Preferred Trip Date", min_value=date.today())
    trip_type = st.selectbox("Trip Type", ["Daily Journey", "Hourly Rental"])

    if trip_type == "Daily Journey":
        st.write("**Daily Journey Details:**")
        num_people = st.number_input("Number of People", min_value=1, step=1)
        cost_per_person = 45
        total_cost = num_people * cost_per_person
        advance_payment = total_cost * 0.3  # 30% advance payment

        st.write(f"<span class='monetary-value'>Total Cost for {num_people} People: ${total_cost} USD</span>", unsafe_allow_html=True)
        st.write(f"<span class='monetary-value'>Advance Payment Required: ${advance_payment} USD</span>", unsafe_allow_html=True)

    elif trip_type == "Hourly Rental":
        st.write("**Hourly Rental Details:**")
        num_people = st.number_input("Number of People", min_value=1, step=1)
        num_hours = st.number_input("Number of Hours", min_value=1, step=1)
        cost_per_hour = 300
        base_cost = num_hours * cost_per_hour
        st.write(f"<span class='monetary-value'>Base Cost for {num_hours} Hours: ${base_cost} USD</span>", unsafe_allow_html=True)

        st.write("Choose Additions:")
        food = st.checkbox("Food")
        jetski = st.checkbox("Jet Ski")
        flyboard = st.checkbox("Flyboard")
        diving = st.checkbox("Diving")

        total_cost = base_cost
        if food:
            total_cost += 50
        if jetski:
            total_cost += 100
        if flyboard:
            total_cost += 150
        if diving:
            total_cost += 200

        advance_payment = total_cost * 0.3  # 30% advance payment

        st.write(f"<span class='monetary-value'>Total Cost with Additions: ${total_cost} USD</span>", unsafe_allow_html=True)
        st.write(f"<span class='monetary-value'>Advance Payment Required: ${advance_payment} USD</span>", unsafe_allow_html=True)

    payment_method = st.selectbox("Payment Method", ["Pay by Card", "Pay on the Day"])
    additional_info = st.text_area("Additional Information")

    if payment_method == "Pay by Card":
        st.write("**Payment Details:**")
        card_number = st.text_input("Card Number")
        exp_month = st.number_input("Expiration Month (MM)", min_value=1, max_value=12, step=1)
        exp_year = st.number_input("Expiration Year (YYYY)", min_value=date.today().year, step=1)
        cvc = st.text_input("CVC")

    if st.button("Submit", key="submit", help="Click to submit your booking request"):
        if payment_method == "Pay by Card":
            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(advance_payment * 100),  # Amount in cents
                    currency='usd',
                    payment_method_data={
                        'type': 'card',
                        'card': {
                            'number': card_number,
                            'exp_month': exp_month,
                            'exp_year': exp_year,
                            'cvc': cvc,
                        },
                    },
                    confirm=True,
                )
                st.write("Payment successful!")
            except stripe.error.CardError as e:
                st.write(f"Payment error: {e.user_message}")

        booking_details = f"""
        Name: {name}
        Email: {email}
        Phone Number: {phone}
        Preferred Trip Date: {trip_date}
        Trip Type: {trip_type}
        """
        if trip_type == "Daily Journey":
            booking_details += f"""
            Number of People: {num_people}
            Total Cost: ${total_cost} USD
            Advance Payment: ${advance_payment} USD
            """
        elif trip_type == "Hourly Rental":
            additions = [opt for opt, val in [('Food', food), ('Jet Ski', jetski), ('Flyboard', flyboard), ('Diving', diving)] if val]
            booking_details += f"""
            Number of People: {num_people}
            Number of Hours: {num_hours}
            Base Cost: ${base_cost} USD
            Additions: {', '.join(additions)}
            Total Cost with Additions: ${total_cost} USD
            Advance Payment: ${advance_payment} USD
            """

        booking_details += f"""
        Payment Method: {payment_method}
        Additional Information: {additional_info}
        """

        send_email("New Booking Request", booking_details)
        st.write("Thank you for your booking request! We will get back to you shortly.")
        st.write("Booking Details:")
        st.write(booking_details)

    st.markdown('</div>', unsafe_allow_html=True)


# ---- SOCIAL MEDIA LINKS ----
st.write("---")
st.header("Follow Us on Social Media")
st.write("##")
st.markdown(
    """
    <style>
    .social-buttons {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 20px;
    }
    .social-buttons a {
        text-decoration: none;
    }
    .social-buttons img {
        border-radius: 50%;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        transition: transform 0.3s ease;
    }
    .social-buttons img:hover {
        transform: scale(1.1);
    }
    </style>
    <div class="social-buttons">
        <a href="https://www.facebook.com" target="_blank">
            <img src="https://img.shields.io/badge/Facebook-blue?style=for-the-badge&logo=facebook" alt="Facebook">
        </a>
        <a href="https://www.instagram.com" target="_blank">
            <img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram">
        </a>
        <a href="https://www.twitter.com" target="_blank">
            <img src="https://img.shields.io/badge/Twitter-blue?style=for-the-badge&logo=twitter" alt="Twitter">
        </a>
    </div>
    """,
    unsafe_allow_html=True
    )

        


# ---- INTERACTIVE MAP ----
with st.container():
    st.write("---")
    st.header("Our Location: MARINA AGADIR")
    st.write("##")

    # Create a map centered around Marina Agadir
    m = folium.Map(location=[30.4266, -9.6225], zoom_start=15, tiles='Stamen Terrain')

    # Add marker cluster
    marker_cluster = MarkerCluster().add_to(m)

    # Add marker for Marina Agadir with a custom icon
    folium.Marker(
        [30.4266, -9.6225],
        popup="""
        <strong>MARINA AGADIR</strong><br>
        One of the most beautiful marinas in Morocco, offering various facilities and services.
        """,
        tooltip="MARINA AGADIR",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(marker_cluster)

    # Add a legend to the map
    legend_html = '''
    <div style="
    position: fixed; 
    bottom: 50px; left: 50px; width: 220px; height: 90px; 
    border:2px solid grey; z-index:9999; font-size:14px;
    background-color:white;
    padding: 10px;
    ">
    &nbsp; <b>Legend</b> <br>
    &nbsp; <i class="fa fa-map-marker fa-2x" style="color:blue"></i>&nbsp; MARINA AGADIR
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Display the map in the Streamlit app
    st_folium(m, width=800, height=600)




# ---- CONTACT ----
def local_css():
    st.markdown(
        """
        <style>
        .contact-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f5f5f5;
            padding: 50px;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        }
        .contact-header {
            text-align: center;
            margin-bottom: 40px;
        }
        .contact-header h1 {
            font-size: 2.5em;
            color: #333;
            margin-bottom: 10px;
        }
        .contact-header p {
            font-size: 1.1em;
            color: #666;
            margin: 0;
        }
        .contact-form {
            display: flex;
            flex-direction: column;
            gap: 20px;
            max-width: 600px;
            width: 100%;
        }
        .contact-form input, .contact-form textarea {
            width: 100%;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #ddd;
            font-size: 1em;
            color: #333;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
            transition: border-color 0.3s, box-shadow 0.3s;
        }
        .contact-form input:focus, .contact-form textarea:focus {
            border-color: #ffd700; /* Luxurious gold */
            box-shadow: 0 0 5px rgba(255, 215, 0, 0.5);
            outline: none;
        }
        .contact-form button {
            background-color: #ffd700; /* Luxurious gold */
            color: #fff;
            border: none;
            padding: 15px;
            border-radius: 8px;
            font-size: 1.1em;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.2s;
        }
        .contact-form button:hover {
            background-color: #e5b700;
            transform: translateY(-2px);
        }
        .contact-image {
            border-radius: 15px;
            max-width: 100%;
            height: auto;
            object-fit: cover;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .contact-info {
            text-align: center;
            margin-top: 20px;
        }
        .contact-info p {
            margin: 10px 0;
            font-size: 1.1em;
            color: #333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

with st.container():
    # Load local CSS
    local_css()
    
    st.markdown('<div class="contact-container">', unsafe_allow_html=True)
    
    # Contact Header
    st.markdown('<div class="contact-header">', unsafe_allow_html=True)
    st.markdown("<h1>Get In Touch With Us</h1>", unsafe_allow_html=True)
    st.markdown("<p>We'd love to hear from you! Fill out the form below, and we'll get back to you as soon as possible.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Contact Form and Image
    left_column, right_column = st.columns([1, 1], gap="large")
    
    with left_column:
        st.markdown(
            """
            <form action="https://formsubmit.co/yassinechmirrou1@gmail.com" method="POST" class="contact-form">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Your Name" required>
                <input type="email" name="email" placeholder="Your Email" required>
                <textarea name="message" placeholder="Your Message" rows="6" required></textarea>
                <button type="submit">Send Message</button>
            </form>
            """, unsafe_allow_html=True
        )
    
    with right_column:
        st.markdown(
            """
            <img src="/path/to/your/image.jpg" alt="Contact Image" class="contact-image">
            """, unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
