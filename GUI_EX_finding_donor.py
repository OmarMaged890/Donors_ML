import tkinter as tk
from tkinter import messagebox
import joblib
import pandas as pd

# Load the trained model
model = joblib.load("model_pickel")  

# Create the main window
root = tk.Tk()
root.title("Donor Prediction Tool")  # Title of the window
root.geometry("500x400")  # Set window size (500 pixels wide by 400 pixels high)
root.configure(bg="#f0f8ff")  # Set background color (Alice Blue)

# Function to make predictions
def predict_donor():  # called when the user clicks the "Predict" button
    try:
        # Get input values
        age = float(age_entry.get()) # Retrieves the value entered by the user
        hours_per_week = float(hours_entry.get()) # Retrieves the value entered by the user
        capital_gain = float(capital_gain_entry.get()) # Retrieves the value entered by the user
        marital_status = int(marital_entry.get()) # Retrieves the value entered by the user
        education_number = int(education_entry.get()) # Retrieves the value entered by the user

        # Validate inputs
        if age < 0 or hours_per_week < 0 or capital_gain < 0:
            messagebox.showerror("Input Error", "Age, Hours, and Capital Gain must be non-negative.")
            return
        if marital_status not in [0, 1]:
            messagebox.showerror("Input Error", "Marital Status must be 1 (Yes) or 0 (No).")
            return
        if education_number <= 0:
            messagebox.showerror("Input Error", "Education Number must be positive.")
            return

        # Create input data with only top 5 features
        input_data = pd.DataFrame({
            'age': [age],
            'hours-per-week': [hours_per_week],
            'capital-gain': [capital_gain],
            'marital-status_ Married-civ-spouse': [marital_status],
            'education-num': [education_number]
        })

        # Add default values for missing features
        all_features = model.feature_names_in_  # Get features the model expects
        for feature in all_features:
            if feature not in input_data.columns:
                input_data[feature] = 0  # Default to 0 for unused features

        # Ensure column order matches the model's expected order
        input_data = input_data[all_features]

        # Make prediction
        prediction = model.predict(input_data)[0]

        # Show result
        result = "Likely Donor" if prediction == 1 else "Not a Donor"
        messagebox.showinfo("Prediction Result", f"The person is: {result}")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical inputs.")
    except FileNotFoundError:
        messagebox.showerror("File Error", "Model file not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Define common styles
label_style = {"bg": "#f0f8ff", "fg": "#333333", "font": ("Helvetica", 10, "bold")}
entry_style = {"bg": "#ffffff", "fg": "#000000", "highlightbackground": "#00008b"}
button_style = {"bg": "#4682b4", "fg": "#ffffff", "font": ("Helvetica", 12, "bold")}

# Label and Entry for Age
age_label = tk.Label(root, text="Age:", **label_style)
age_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
age_entry = tk.Entry(root, **entry_style)
age_entry.grid(row=0, column=1, padx=10, pady=5)

# Label and Entry for Hours Per Week
hours_label = tk.Label(root, text="Hours Per Week:", **label_style)
hours_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
hours_entry = tk.Entry(root, **entry_style)
hours_entry.grid(row=1, column=1, padx=10, pady=5)

# Label and Entry for Capital Gain
capital_gain_label = tk.Label(root, text="Capital Gain:", **label_style)
capital_gain_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
capital_gain_entry = tk.Entry(root, **entry_style)
capital_gain_entry.grid(row=2, column=1, padx=10, pady=5)

# Label and Entry for Marital Status
marital_label = tk.Label(root, text="Married (1 = Yes, 0 = No):", **label_style)
marital_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
marital_entry = tk.Entry(root, **entry_style)
marital_entry.grid(row=3, column=1, padx=10, pady=5)

# Label and Entry for Education Number
education_label = tk.Label(root, text="Education Number:", **label_style)
education_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
education_entry = tk.Entry(root, **entry_style)
education_entry.grid(row=4, column=1, padx=10, pady=5)

# Predict Button
predict_button = tk.Button(root, text="Predict", command=predict_donor, **button_style)
predict_button.grid(row=5, column=0, columnspan=2, pady=10)

# Start the GUI event loop
root.mainloop()
