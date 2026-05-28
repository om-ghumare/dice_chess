import 'package:dicechess_v2_client/src/app.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('app boots to home', (tester) async {
    await tester.pumpWidget(const DiceChessApp());
    expect(find.text('Dice Chess'), findsOneWidget);
    expect(find.text('Enter Lobby'), findsOneWidget);
  });
}
