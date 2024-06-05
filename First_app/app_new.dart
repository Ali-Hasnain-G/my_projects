                    //yaml 
name: pharmacy_app
description: A comprehensive Flutter pharmacy app.

publish_to: 'none'

version: 1.0.0+1

environment:
  sdk: '>=2.12.0 <3.0.0'

dependencies:
  flutter:
    sdk: flutter
  flutter_spinkit: ^5.1.0
  csv: ^5.0.0
  path_provider: ^2.0.11
  provider: ^6.0.5
  shared_preferences: ^2.0.15
  intl: ^0.17.0
  http: ^0.14.0

  cupertino_icons: ^1.0.2

dev_dependencies:
  flutter_test:
    sdk: flutter

flutter:
  uses-material-design: true
  assets:
    - assets/products.csv

       // full code
import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'csv_loader.dart';
import 'models/medication.dart';
import 'screens/home_page.dart';
import 'screens/login_page.dart';
import 'screens/products_page.dart';
import 'screens/reminders_page.dart';
import 'screens/signup_page.dart';
import 'screens/symptom_checker_page.dart';
import 'screens/health_tracking_page.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => MedicationProvider(),
      child: MaterialApp(
        title: 'Pharmacy App',
        theme: ThemeData(
          primarySwatch: Colors.green,
          visualDensity: VisualDensity.adaptivePlatformDensity,
        ),
        home: LoginPage(),
        routes: {
          '/home': (context) => HomePage(),
          '/products': (context) => ProductsPage(),
          '/contact': (context) => ContactPage(),
          '/login': (context) => LoginPage(),
          '/signup': (context) => SignUpPage(),
          '/reminders': (context) => RemindersPage(),
          '/symptom_checker': (context) => SymptomCheckerPage(),
          '/health_tracking': (context) => HealthTrackingPage(),
        },
      ),
    );
  }
}

class Footer extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.green,
      padding: EdgeInsets.all(16.0),
      child: Text(
        '© 2024 Pharmacy App. All rights reserved.',
        textAlign: TextAlign.center,
        style: TextStyle(color: Colors.white),
      ),
    );
  }
}

// models

import 'package:flutter/foundation.dart';

class Medication {
  final String name;
  final double dosage;
  final String unit;
  final DateTime time;

  Medication({
    required this.name,
    required this.dosage,
    required this.unit,
    required this.time,
  });
}

// MedicationProvider

class MedicationProvider with ChangeNotifier {
  List<Medication> _medications = [];

  List<Medication> get medications => _medications;

  void addMedication(Medication medication) {
    _medications.add(medication);
    notifyListeners();
  }

  void removeMedication(Medication medication) {
    _medications.remove(medication);
    notifyListeners();
  }
}

// screens

// RemindersPage

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../models/medication.dart';

class RemindersPage extends StatefulWidget {
  @override
  _RemindersPageState createState() => _RemindersPageState();
}

class _RemindersPageState extends State<RemindersPage> {
  final _formKey = GlobalKey<FormState>();
  String _name = '';
  double _dosage = 0;
  String _unit = 'mg';
  DateTime _time = DateTime.now();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Medicine Reminders'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                decoration: InputDecoration(labelText: 'Medicine Name'),
                onSaved: (value) {
                  _name = value!;
                },
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Dosage'),
                keyboardType: TextInputType.number,
                onSaved: (value) {
                  _dosage = double.parse(value!);
                },
              ),
              DropdownButtonFormField<String>(
                value: _unit,
                items: ['mg', 'ml', 'g'].map((String value) {
                  return DropdownMenuItem<String>(
                    value: value,
                    child: Text(value),
                  );
                }).toList(),
                onChanged: (value) {
                  setState(() {
                    _unit = value!;
                  });
                },
              ),
              TextButton(
                onPressed: () async {
                  final TimeOfDay? picked = await showTimePicker(
                    context: context,
                    initialTime: TimeOfDay.fromDateTime(_time),
                  );
                  if (picked != null) {
                    setState(() {
                      _time = DateTime(
                        _time.year,
                        _time.month,
                        _time.day,
                        picked.hour,
                        picked.minute,
                      );
                    });
                  }
                },
                child: Text('Pick Time: ${DateFormat.Hm().format(_time)}'),
              ),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    _formKey.currentState!.save();
                    Provider.of<MedicationProvider>(context, listen: false).addMedication(
                      Medication(
                        name: _name,
                        dosage: _dosage,
                        unit: _unit,
                        time: _time,
                      ),
                    );
                    Navigator.pop(context);
                  }
                },
                child: Text('Add Reminder'),
              ),
              Expanded(
                child: Consumer<MedicationProvider>(
                  builder: (context, provider, child) {
                    return ListView.builder(
                      itemCount: provider.medications.length,
                      itemBuilder: (context, index) {
                        final medication = provider.medications[index];
                        return ListTile(
                          title: Text('${medication.name} (${medication.dosage}${medication.unit})'),
                          subtitle: Text('Time: ${DateFormat.Hm().format(medication.time)}'),
                          trailing: IconButton(
                            icon: Icon(Icons.delete),
                            onPressed: () {
                              provider.removeMedication(medication);
                            },
                          ),
                        );
                      },
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// SymptomCheckerPage

import 'package:flutter/material.dart';

class SymptomCheckerPage extends StatefulWidget {
  @override
  _SymptomCheckerPageState createState() => _SymptomCheckerPageState();
}

class _SymptomCheckerPageState extends State<SymptomCheckerPage> {
  final _formKey = GlobalKey<FormState>();
  String _symptoms = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Symptom Checker'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                decoration: InputDecoration(labelText: 'Enter your symptoms'),
                maxLines: 4,
                onSaved: (value) {
                  _symptoms = value!;
                },
              ),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    _formKey.currentState!.save();

// Implement symptom checking logic

                    showDialog(
                      context: context,
                      builder: (context) => AlertDialog(
                        title: Text('Possible Conditions'),
                        content: Text('Based on your symptoms, these are the possible conditions:\n\n- Condition A\n- Condition B\n- Condition C'),
                        actions: [
                          TextButton(
                            onPressed: () {
                              Navigator.of(context).pop();
                            },
                            child: Text('OK'),
                          ),
                        ],

// HealthTrackingPage

import 'package:flutter/material.dart';

class HealthTrackingPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Health Tracking'),
      ),
      body: Center(
        child: Text('Health Tracking Page'),
      ),
    );
  }
}

// PrescriptionRefillsPage

import 'package:flutter/material.dart';

class PrescriptionRefillsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Prescription Refills'),
      ),
      body: Center(
        child: Text('Prescription Refills Page'),
      ),
    );
  }
}

// PharmacyLocatorPage

import 'package:flutter/material.dart';

class PharmacyLocatorPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Pharmacy Locator'),
      ),
      body: Center(
        child: Text('Pharmacy Locator Page'),
      ),
    );
  }
}

// InsuranceIntegrationPage

import 'package:flutter/material.dart';

class InsuranceIntegrationPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Insurance Integration'),
      ),
      body: Center(
        child: Text('Insurance Integration Page'),
      ),
    );
  }
}

// add more
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../models/medication.dart';

class RemindersPage extends StatefulWidget {
  @override
  _RemindersPageState createState() => _RemindersPageState();
}

class _RemindersPageState extends State<RemindersPage> {
  final _formKey = GlobalKey<FormState>();
  String _name = '';
  double _dosage = 0;
  String _unit = 'mg';
  DateTime _time = DateTime.now();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Medicine Reminders'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                decoration: InputDecoration(labelText: 'Medicine Name'),
                onSaved: (value) {
                  _name = value!;
                },
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Dosage'),
                keyboardType: TextInputType.number,
                onSaved: (value) {
                  _dosage = double.parse(value!);
                },
              ),
              DropdownButtonFormField<String>(
                value: _unit,
                items: ['mg', 'ml', 'g'].map((String value) {
                  return DropdownMenuItem<String>(
                    value: value,
                    child: Text(value),
                  );
                }).toList(),
                onChanged: (value) {
                  setState(() {
                    _unit = value!;
                  });
                },
              ),
              TextButton(
                onPressed: () async {
                  final TimeOfDay? picked = await showTimePicker(
                    context: context,
                    initialTime: TimeOfDay.fromDateTime(_time),
                  );
                  if (picked != null) {
                    setState(() {
                      _time = DateTime(
                        _time.year,
                        _time.month,
                        _time.day,
                        picked.hour,
                        picked.minute,
                      );
                    });
                  }
                },
                child: Text('Pick Time: ${DateFormat.Hm().format(_time)}'),
              ),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    _formKey.currentState!.save();
                    Provider.of<MedicationProvider>(context, listen: false).addMedication(
                      Medication(
                        name: _name,
                        dosage: _dosage,
                        unit: _unit,
                        time: _time,
                      ),
                    );
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text('Reminder added successfully'),
                        duration: Duration(seconds: 2),
                      ),
                    );
                    Navigator.pop(context);
                  }
                },
                child: Text('Add Reminder'),
              ),
              SizedBox(height: 20),
              Expanded(
                child: Consumer<MedicationProvider>(
                  builder: (context, provider, child) {
                    return ListView.builder(
                      itemCount: provider.medications.length,
                      itemBuilder: (context, index) {
                        final medication = provider.medications[index];
                        return ListTile(
                          title: Text('${medication.name} (${medication.dosage}${medication.unit})'),
                          subtitle: Text('Time: ${DateFormat.Hm().format(medication.time)}'),
                          trailing: IconButton(
                            icon: Icon(Icons.delete),
                            onPressed: () {
                              provider.removeMedication(medication);
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(
                                  content: Text('Reminder deleted'),
                                  duration: Duration(seconds: 2),
                                ),
                              );
                            },
                          ),
                        );
                      },
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// MedicationManagementPage

import 'package:flutter/material.dart';

class MedicationManagementPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Medication Management'),
      ),
      body: Center(
        child: Text('Medication Management Page'),
      ),
    );
  }
}

// TelemedicinePage

import 'package:flutter/material.dart';

class TelemedicinePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Telemedicine'),
      ),
      body: Center(
        child: Text('Telemedicine Page'),
      ),
    );
  }
}

// ReviewsRatingsPage

import 'package:flutter/material.dart';

class ReviewsRatingsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Reviews and Ratings'),
      ),
      body: Center(
        child: Text('Reviews and Ratings Page'),
      ),
    );
  }
}

// import 'package:flutter/material.dart';

class PersonalizedRecommendationsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Personalized Recommendations'),
      ),
      body: Center(
        child: Text('Personalized Recommendations Page'),
      ),
    );
  }
}

// PushNotificationsPage

import 'package:flutter/material.dart';

class PushNotificationsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Push Notifications'),
      ),
      body: Center(
        child: Text('Push Notifications Page'),
      ),
    );
  }
}

// SecureMessagingPage

import 'package:flutter/material.dart';

class SecureMessagingPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Secure Messaging'),
      ),
      body: Center(
        child: Text('Secure Messaging Page'),
      ),
    );
  }
}

import 'package:flutter/material.dart';

class ProductsPage extends StatefulWidget {
  @override
  _ProductsPageState createState() => _ProductsPageState();
}

class _ProductsPageState extends State<ProductsPage> {
  // Sample product data
  List<Product> _products = [
    Product(name: 'Product 1', price: 10.0),
    Product(name: 'Product 2', price: 15.0),
    Product(name: 'Product 3', price: 20.0),
    Product(name: 'Product 4', price: 25.0),
  ];

  // Function to sort products by price

  void _sortProductsByPrice(bool ascending) {
    setState(() {
      if (ascending) {
        _products.sort((a, b) => a.price.compareTo(b.price));
      } else {
        _products.sort((a, b) => b.price.compareTo(a.price));
      }
    });
  }

  // Function to filter products by price

  void _filterProductsByPrice(double minPrice, double maxPrice) {
    setState(() {
      _products = _products.where((product) => product.price >= minPrice && product.price <= maxPrice).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Products'),
        actions: [
          IconButton(
            icon: Icon(Icons.sort),
            onPressed: () {
              showModalBottomSheet(
                context: context,
                builder: (BuildContext context) {
                  return Column(
                    mainAxisSize: MainAxisSize.min,
                    children: <Widget>[
                      ListTile(
                        leading: Icon(Icons.arrow_upward),
                        title: Text('Sort by Price (Low to High)'),
                        onTap: () {
                          Navigator.pop(context);
                          _sortProductsByPrice(true);
                        },
                      ),
                      ListTile(
                        leading: Icon(Icons.arrow_downward),
                        title: Text('Sort by Price (High to Low)'),
                        onTap: () {
                          Navigator.pop(context);
                          _sortProductsByPrice(false);
                        },
                      ),
                    ],
                  );
                },
              );
            },
          ),
          IconButton(
            icon: Icon(Icons.filter_list),
            onPressed: () {
              showDialog(
                context: context,
                builder: (BuildContext context) {
                  return AlertDialog(
                    title: Text('Filter by Price'),
                    content: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        TextField(
                          decoration: InputDecoration(labelText: 'Min Price'),
                          keyboardType: TextInputType.number,
                          onChanged: (value) => _minPrice = double.tryParse(value) ?? 0,
                        ),
                        TextField(
                          decoration: InputDecoration(labelText: 'Max Price'),
                          keyboardType: TextInputType.number,
                          onChanged: (value) => _maxPrice = double.tryParse(value) ?? double.infinity,
                        ),
                      ],
                    ),
                    actions: <Widget>[
                      TextButton(
                        onPressed: () {
                          Navigator.of(context).pop();
                        },
                        child: Text('Cancel'),
                      ),
                      TextButton(
                        onPressed: () {
                          Navigator.of(context).pop();
                          _filterProductsByPrice(_minPrice, _maxPrice);
                        },
                        child: Text('Apply'),
                      ),
                    ],
                  );
                },
              );
            },
          ),
        ],
      ),
      body: ListView.builder(
        itemCount: _products.length,
        itemBuilder: (context, index) {
          final product = _products[index];
          return ListTile(
            title: Text(product.name),
            subtitle: Text('Price: \$${product.price.toStringAsFixed(2)}'),
          );
        },
      ),
    );
  }
}

class Product {
  final String name;
  final double price;

  Product({required this.name, required this.price});
}

//  whatsapp

import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Home'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            showDialog(
              context: context,
              builder: (BuildContext context) {
                return AlertDialog(
                  title: Text('Contact or Hire'),
                  content: SingleChildScrollView(
                    child: ListBody(
                      children: <Widget>[
                        ListTile(
                          leading: Icon(Icons.message),
                          title: Text('Contact a Doctor via WhatsApp'),
                          onTap: () {
                            // Open WhatsApp chat with the doctor's number
                            // You may need to integrate a package like url_launcher for this
                            Navigator.of(context).pop();
                          },
                        ),
                        ListTile(
                          leading: Icon(Icons.person_add),
                          title: Text('Hire a Doctor'),
                          onTap: () {
                            // Navigate to the screen where users can hire a doctor
                            Navigator.of(context).pop();
                            Navigator.pushNamed(context, '/hire_doctor');
                          },
                        ),
                      ],
                    ),
                  ),
                );
              },
            );
          },
          child: Text('Contact or Hire a Doctor'),
        ),
      ),
    );
  }
}

// hire_doctor_page

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'screens/home_page.dart';
import 'screens/hire_doctor_page.dart'; // Import the new page

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Pharmacy App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => HomePage(),
        '/hire_doctor': (context) => HireDoctorPage(), // Add the route for the new page
      },
    );
  }
}

// HireDoctorPage

import 'package:flutter/material.dart';

class HireDoctorPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Hire a Doctor'),
      ),
      body: Center(
        child: Text('Hire a Doctor Page'),
      ),
    );
  }
}
