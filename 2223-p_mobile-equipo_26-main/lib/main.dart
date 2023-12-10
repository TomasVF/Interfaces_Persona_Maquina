import 'dart:convert';
import 'dart:ffi';

import 'package:flutter/material.dart';
import 'package:p_mobile/edamam.dart';

const List<String> listDiet = <String>[
  '',
  'balanced',
  'high-fiber',
  'high-protein',
  'low-carb',
  'low-fat'
];
const List<String> listCuisineType = <String>[
  '',
  'American',
  'Asian',
  'British',
  'Caribbean',
  'Central Europe',
  'Chinese',
  'Eastern Europe',
  'French',
  'Indian',
  'Italian',
  'Japanese',
  'Kosher',
  'Mediterranean',
  'Mexican',
  'Middle Eastern',
  'Nordic',
  'South American',
  'South East Asian'
];
const List<String> listMealType = <String>[
  '',
  'Breakfast',
  'Dinner',
  'Lunch',
  'Snack',
  'Teatime'
];

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String? dropdownValueDiet;
  String? dropdownValueCuisineType;
  String? dropdownValueMealType;
  final myController = TextEditingController();

  @override
  void dispose() {
    myController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Recetas App'),
      ),
      body: Container(
        margin: const EdgeInsets.only(top: 100, left: 20, right: 20),
        child: GridView.count(
          childAspectRatio: 2.48,
          crossAxisCount: 2,
          children: [
            TextField(
              controller: myController,
              style: const TextStyle(color: Colors.black, fontSize: 18.0),
              decoration: const InputDecoration(
                labelText: 'Palabras clave',
              ),
            ),
            DropdownButton<String>(
              hint: const Text('Diets'),
              value: dropdownValueDiet,
              menuMaxHeight: 200.0,
              style: const TextStyle(color: Colors.black, fontSize: 18.0),
              underline: Container(
                height: 2,
                color: Colors.black12,
              ),
              onChanged: (String? value) {
                setState(() {
                  dropdownValueDiet = value!;
                });
              },
              items: listDiet.map<DropdownMenuItem<String>>((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Text(value),
                );
              }).toList(),
            ),
            DropdownButton<String>(
              hint: const Text('Cuisine types'),
              value: dropdownValueCuisineType,
              menuMaxHeight: 200.0,
              style: const TextStyle(color: Colors.black, fontSize: 18.0),
              underline: Container(
                height: 2,
                color: Colors.black12,
              ),
              onChanged: (String? value) {
                setState(() {
                  dropdownValueCuisineType = value!;
                });
              },
              items:
                  listCuisineType.map<DropdownMenuItem<String>>((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Text(value),
                );
              }).toList(),
            ),
            DropdownButton<String>(
              hint: const Text('Meal types'),
              menuMaxHeight: 200.0,
              value: dropdownValueMealType,
              style: const TextStyle(color: Colors.black, fontSize: 18.0),
              underline: Container(
                height: 2,
                color: Colors.black12,
              ),
              onChanged: (String? value) {
                setState(() {
                  dropdownValueMealType = value!;
                });
              },
              items: listMealType.map<DropdownMenuItem<String>>((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Text(value),
                );
              }).toList(),
            ),
            const Text(
                style: TextStyle(color: Colors.black, fontSize: 18.0),
                'Es necesario indicar algún campo para recibir resultados'),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (BuildContext context) {
                    return RecetasListScreen(
                        diet: dropdownValueDiet,
                        cuisineType: dropdownValueCuisineType,
                        mealType: dropdownValueMealType,
                        keywords: myController.text);
                  }),
                );
              },
              child: const Text('Search'),
            ),
          ],
        ),
      ),
    );
  }
}

class RecetasListScreen extends StatelessWidget {
  String? diet;
  String? cuisineType;
  String? mealType;
  String? keywords;

  RecetasListScreen(
      {super.key,
      this.diet,
      this.cuisineType,
      this.mealType,
      this.keywords});
  @override
  Widget build(BuildContext context) {
    if(keywords == null){
      keywords == "";
    }
    if(diet == null){
      diet = "";
    }
    if(cuisineType == null){
      cuisineType = "";
    }
    if(mealType == null){
      mealType = "";
    }
    return Scaffold(
      appBar: AppBar(
        title: Text(keywords!),
      ),
      body: Center(
        child: FutureBuilder<RecipeBlock?>(
          future: search_recipes(keywords!, diet!, cuisineType!, mealType!),
          builder:
              (BuildContext context, AsyncSnapshot<RecipeBlock?> snapshot) {
            if (snapshot.hasError) {
              return Center(
                child: SingleChildScrollView(
                  child: Column(
                    children: const <Widget>[
                      Text(
                        style: TextStyle(fontSize: 25),
                          'There was a network error'),
                    ],
                  ),
                ),
              );
            } else if (snapshot.connectionState != ConnectionState.done) {
              return const Center(
                child: CircularProgressIndicator(),
              );
            } else if(snapshot.data == null || snapshot.data!.recipes == null){
              return Center(
                child: SingleChildScrollView(
                  child: Column(
                    children: const <Widget>[
                      Text(
                          style: TextStyle(fontSize: 25),
                          'There is no result for those options'),
                    ],
                  ),
                ),
              );
            }else {
              List<Recipe> data = snapshot.data!.recipes!;
              return ListView.builder(
                  itemCount: data.length,
                  itemBuilder: (BuildContext context, int i) => ListTile(
                        title: Text(data[i].label.toString()),
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (BuildContext context) {
                              return Receta(receta: data[i]);
                            }),
                          );
                        },
                      ));
            }
          },
        ),
      ),
    );
  }
}

class Receta extends StatelessWidget {
  final Recipe receta;
  const Receta({super.key, required this.receta});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(receta.label.toString()),
      ),
      body: Center(
        child: Column(
          children: [
            Image.network(
                fit: BoxFit.fill, width: 200, receta.thumbnail.toString()),
            Expanded(
              child: SingleChildScrollView(
                scrollDirection: Axis.vertical,
                child: Text(
                  receta.toString(),
                  style: const TextStyle(color: Colors.black, fontSize: 18.0),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

