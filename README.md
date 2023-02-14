# Power House ⚡ #

Dies ist der aktuelle Stand der Webapp meiner Masterthesis. Folgende Funktionen sind bereits implementiert und können ausprobiert werden:

### NEUE FUNKTIONEN 🎉 ###
> - Mit einem Button in der Navigationsleiste kann ein Beispielnetz erstellt werden.
> - Durch Klicken auf die Elemente kann Last/Einspeisung ausgewählt und die Leistung eingestellt werden.
> - Mit dem Button "Berechnen" wird eine Leistungsflussberechnung durchgeführt und die Ergebnisse im Netz angezeigt.
> - Wird ein Element mit einem Trafo verbunden, dessen Spannungsebene nicht klar definiert ist (z.B. PV), wird in einem Dialog die Spannungsebene abgefragt.

⚠️Die Richtung der Pfeile auf den Leitungen im Netz stimmt nicht immer!

Details zur Berechnung des Graphen: Siehe unten

### Aktueller Fortschritt: ###
- [x]  Aus erstelltem Netz Graphenstruktur zur späteren Berechnung erstellen.
- [x]  Transformatoren als zwei Knoten darstellen und Kanten richtig verbinden.
- [x]  Schleifen und Parallelschaltungen im Netz mit dem Graphen erkennen.
- [x]  Aus Inzidenzmatrix des Graphen lineares Gleichungssystem erstellen.
- [ ]  Zusätzliche Gleichungen für Schleifen und parallele Leitungen zum Gleichungssystem hinzufügen.
- [x]  Lastgänge-/Einspeisungen in Elementen hinterlegen.
- [x]  Erste Flussberechnung durch Lösen des Gleichungssystems durchführen.
- [ ]  Richtung Leitungspfeile richtig anpassen.
- [ ]  Last/Einspeisung als Zeitreihe hinterlegen.
- [ ]  Leistungsfluss für Zeitreihen berechnen.

### Funktionen: ###
- Netzelemente können über die Buttons links hinzugefügt werden.
- Netzelemente können auf der Arbeitsfläche per Drag&Drop verschoben werden.
- Zwischen zwei Netzelementen kann wie folgt ein Kabel gezogen werden:
  - Auf das Freileitungssymbol unten links klicken.
  - Nacheinander die zu verbindenden Elemente anklicken.
  - Leitungsmodus durch erneutes Klicken auf das Freileitungssymbol beenden.
  - Es wird überprüft, ob die beiden Elemente miteinander verbunden werden dürfen. Wenn nicht, wird eine Fehlermeldung angezeigt.
- Durch Klicken auf ein Netzelement oder Kabel öffnet sich ein Fenster. In diesem wird man das Element später bearbeiten können.
- Die Netzelemente und Kabel können im Bearbeitungs-Dialog wieder gelöscht werden. Wird ein Netzelement gelöscht, werden auch die verbundenen Kabel entfernt.

#### Berechnung des Graphen: ####
Jedes Element des gezeichneten Netzes wird in einen Graphenknoten mit seinen Eigenschaften übertragen. Für jeden Transformator wird ein weiterer Knoten erstellt. 
  Ein Trafo wird also durch zwei Knoten repräsentiert, dies dient zum einen zur Darstellung von Anschlüssen an Ober-/Unterspannungsseite. Vor allem kann so aber der 
  Kante zwischen den beiden Knoten eine Impedanz zugewiesen werden, die in der Flussberechnung dann die unterschiedliche Kapazität von parallel geschalteten Trafos berücksichtigt und den Fluss dementsprechend realistisch berechnet.

Fragen und Anregungen gern an mich [per Mail](mailto:felix.husemann@tum.de)
~~~
Stand: 08.02.2023
© Felix Husemann, TUM
~~~