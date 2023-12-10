import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:flutter/material.dart';

// The application under test.
import 'package:p_mobile/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  
  group('end to end test', ()
  {
    testWidgets(
        'search without selecting any option and without using any keyword',
            (WidgetTester tester) async {
              app.main();
              await tester.pumpAndSettle();
              final Finder button = find.text('Search');
              await tester.tap(button);
              await tester.pumpAndSettle();
              expect(find.text('There is no result for those options'), findsOneWidget);
        });
    testWidgets(
        'search using a word that does not exist',
            (WidgetTester tester) async {
          app.main();
          await tester.pumpAndSettle();
          await tester.enterText(find.byType(TextField), 'añhgakjdghñ');
          final Finder button = find.text('Search');
          await tester.tap(button);
          await tester.pumpAndSettle();
          expect(find.text('There is no result for those options'), findsOneWidget);
        });
    testWidgets(
        'search for a recipe',
            (WidgetTester tester) async {
          app.main();
          await tester.pumpAndSettle();
          await tester.enterText(find.byType(TextField), 'bread');
          await tester.pumpAndSettle();
          final Finder button = find.text('Search');
          await tester.tap(button);
          await tester.pumpAndSettle();
          expect(find.byType(ListView), findsOneWidget);
          final Finder recipe = find.byType(ListView);
          await tester.tap(recipe);
          await tester.pumpAndSettle();
          expect(find.byType(Image), findsOneWidget);
          expect(find.byType(Text), findsWidgets);
        });
    testWidgets(
        'search for a recipe and selecting a diet',
            (WidgetTester tester) async {
          app.main();
          await tester.pumpAndSettle();
          await tester.enterText(find.byType(TextField), 'bread');
          final Finder dropdownButton = find.text('Diets');
          await tester.tap(dropdownButton);
          await tester.pumpAndSettle();
          final dropdownItem = find.text('balanced').at(1);
          await tester.tap(dropdownItem);
          await tester.pumpAndSettle();
          final Finder button = find.text('Search');
          await tester.tap(button);
          await tester.pumpAndSettle();
          expect(find.byType(ListView), findsOneWidget);
          final Finder recipe = find.byType(ListView);
          await tester.tap(recipe);
          await tester.pumpAndSettle();
          expect(find.byType(Image), findsOneWidget);
          expect(find.byType(Text), findsWidgets);
        });
  });

}