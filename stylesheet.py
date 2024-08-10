# STYLESHEET = """QWidget {
#     font-family: Arial, sans-serif;
#     font-size: 14px;
#     color: #2c3e50; /* Darker text color for better readability */
#     background-color: #f4f6f9; /* Light background color for the entire window */
# }

# QLabel {
#     color: #34495e; /* Slightly darker shade for labels */
#     font-weight: bold; /* Bold text for labels to make them stand out */
#     padding-bottom: 5px; /* Add padding below labels for better spacing */
# }

# QLineEdit, QDateEdit {
#     border: 1px solid #bdc3c7; /* Light gray border */
#     border-radius: 5px;
#     padding: 8px;
#     background-color: #ffffff; /* White background for input fields */
#     color: #2c3e50; /* Darker text color for input fields */
# }

# QPushButton {
#     background-color: #3498db; /* Soft blue button color */
#     color: white;
#     border: none;
#     border-radius: 5px;
#     padding: 12px;
#     font-weight: bold;
# }

# QPushButton:hover {
#     background-color: #2980b9; /* Darker blue on hover */
# }

# QTableWidget {
#     border: 1px solid #bdc3c7;
#     background-color: #ffffff;
#     gridline-color: #e0e0e0; /* Light gray gridlines for better separation */
# }

# QTableWidget QHeaderView::section {
#     background-color: #3498db; /* Soft blue header color */
#     color: white;
#     font-weight: bold; /* Bold text for headers */
#     padding: 10px; /* Add padding for better spacing */
# }

# QGroupBox {
#     font-weight: bold;
#     border: 2px solid #bdc3c7;
#     border-radius: 5px;
#     margin-bottom: 20px; /* Increased margin for better separation */
#     padding: 10px; /* Added padding inside group boxes */
#     background-color: #ffffff; /* White background for group boxes */
# }

# QGroupBox:title {
#     subcontrol-position: top center;
#     padding: 0px; /* Increased padding for better visibility */
#     background-color: #ecf0f1; /* Light gray background for the title area */
#     color: #3498db; /* Soft blue for the title text */
#     font-size: 16px; /* Increased font size for better readability */
# }

# QCheckBox {
#     padding: 5px;
# }

# QDialogButtonBox {
#     button-layout: QDialogButtonBox::ActionRole;
# }

# QMenuBar {
#     background-color: #3498db; /* Soft blue background color for the menu bar */
#     color: white; /* White text color for the menu items */
# }

# QMenuBar::item {
#     background-color: #3498db; /* Soft blue background color for menu items */
#     color: white; /* White text color for menu items */
# }

# QMenuBar::item:selected {
#     background-color: #2980b9; /* Darker blue for selected menu items */
# }

# QMenu {
#     background-color: #ffffff; /* White background color for menus */
#     border: 1px solid #bdc3c7; /* Light gray border for menus */
# }

# QMenu::item {
#     background-color: #ffffff; /* White background color for menu items */
#     color: #2c3e50; /* Darker text color for menu items */
# }

# QMenu::item:selected {
#     background-color: #3498db; /* Soft blue for selected menu items */
#     color: white; /* White text color for selected menu items */
# }

# QMenu::separator {
#     height: 1px; /* Height of the separator line */
#     background-color: #bdc3c7; /* Light gray color for the separator line */
# }
# """



STYLESHEET = """QWidget {
    font-family: Arial, sans-serif;
    font-size: 14px;
    color: #2c3e50; /* Darker text color for better readability */
    background-color: #f4f6f9; /* Light background color for the entire window */
}

QLabel {
    color: #34495e; /* Slightly darker shade for labels */
    font-weight: bold; /* Bold text for labels to make them stand out */
    padding-bottom: 5px; /* Add padding below labels for better spacing */
}

QLineEdit, QDateEdit {
    border: 1px solid #bdc3c7; /* Light gray border */
    border-radius: 5px;
    padding: 8px;
    background-color: #ffffff; /* White background for input fields */
    color: #2c3e50; /* Darker text color for input fields */
}

QPushButton {
    background-color: #3498db; /* Soft blue button color */
    color: white;
    border: none;
    border-radius: 5px;
    padding: 12px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2980b9; /* Darker blue on hover */
}

QTableWidget {
    border: 1px solid #bdc3c7;
    background-color: #ffffff;
    gridline-color: #e0e0e0; /* Light gray gridlines for better separation */
}

QTableWidget QHeaderView::section {
    background-color: #3498db; /* Soft blue header color */
    color: white;
    font-weight: bold; /* Bold text for headers */
    padding: 10px; /* Add padding for better spacing */
}

QGroupBox {
    font-weight: bold;
    border: 2px solid #bdc3c7;
    border-radius: 5px;
    margin-bottom: 20px; /* Increased margin for better separation */
    padding: 10px; /* Added padding inside group boxes */
    background-color: #ffffff; /* White background for group boxes */
}

QGroupBox:title {
    subcontrol-position: top center;
    padding: 0px; /* Increased padding for better visibility */
    background-color: #ecf0f1; /* Light gray background for the title area */
    color: #3498db; /* Soft blue for the title text */
    font-size: 16px; /* Increased font size for better readability */
}

QCheckBox {
    padding: 5px;
}

QDialogButtonBox {
    button-layout: QDialogButtonBox::ActionRole;
}

QMenuBar {
    background-color: #3498db; /* Soft blue background color for the menu bar */
    color: white; /* White text color for the menu items */
    padding: 50px; /* Ensure padding so it is not obscured */
    z-index: 100; /* Ensure menu bar is on top */
}

QMenuBar::item {
    background-color: #3498db; /* Soft blue background color for menu items */
    color: white; /* White text color for menu items */
}

QMenuBar::item:selected {
    background-color: #2980b9; /* Darker blue for selected menu items */
}

QMenu {
    background-color: #ffffff; /* White background color for menus */
    border: 1px solid #bdc3c7; /* Light gray border for menus */
    padding: 0; /* Remove padding if needed */
}

QMenu::item {
    background-color: #ffffff; /* White background color for menu items */
    color: #2c3e50; /* Darker text color for menu items */
}

QMenu::item:selected {
    background-color: #3498db; /* Soft blue for selected menu items */
    color: white; /* White text color for selected menu items */
}

QMenu::separator {
    height: 1px; /* Height of the separator line */
    background-color: #bdc3c7; /* Light gray color for the separator line */
}
"""
