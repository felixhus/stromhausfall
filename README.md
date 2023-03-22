# Power House ⚡ #

Dies ist der aktuelle Stand der Webapp meiner Masterthesis. Folgende Funktionen sind bereits implementiert und können ausprobiert werden:

### NEUE FUNKTIONEN 🎉 ###
> In dem Tab "Haus 1" kann ein Haus in seinen Räumen frei konfiguriert werden.

### Funktionen Haus: ###

⚠️Nur das Bad funktioniert. Die anderen Räumen werden in Kürze erstellt.
- In jedem Raum befindet sich eine Steckdosenleiste. Über das + kann ein neues Gerät hinzugefügt werden.
- Klickt man auf ein Gerät, öffnet sich rechts ein Menü zur Konfiguration.
- Jedes Gerät kann entweder durch klicken auf die zugehörige Steckdose, oder durch den Schalter im Menu an- oder abgeschaltet werden. Ist es abgeschaltet, wird es in der Berechnung nicht berücksichtigt.
- Der Name des Geräts kann geändert und abgespeichert werden.
- Für jedes Gerät kann aus einer Liste von hinterlegten Lastprofilen über einen Tag gewählt werden.
- Nach dem Speichern wird das Lastprofil angezeigt.
- Mit dem Button "BERECHNEN" wird das resultierende Lastprofil des Hauses berechnet und in Graphen angezeigt.

### Funktionen Netz: ###
- Netzelemente können über die Buttons links hinzugefügt werden.
- Netzelemente können auf der Arbeitsfläche per Drag&Drop verschoben werden.
- Zwischen zwei Netzelementen kann wie folgt ein Kabel gezogen werden:
  - Auf das Freileitungssymbol unten links klicken.
  - Nacheinander die zu verbindenden Elemente anklicken.
  - Leitungsmodus durch erneutes Klicken auf das Freileitungssymbol beenden.
  - Es wird überprüft, ob die beiden Elemente miteinander verbunden werden dürfen. Wenn nicht, wird eine Fehlermeldung angezeigt.
- Durch Klicken auf ein Netzelement oder Kabel öffnet sich ein Fenster. In diesem wird man das Element später bearbeiten können.
- Die Netzelemente und Kabel können im Bearbeitungs-Dialog wieder gelöscht werden. Wird ein Netzelement gelöscht, werden auch die verbundenen Kabel entfernt.
- Mit dem Button "Berechnen" wird eine Leistungsflussberechnung durchgeführt und die Ergebnisse im Netz angezeigt.
- Wird ein Element mit einem Trafo verbunden, dessen Spannungsebene nicht klar definiert ist (z.B. PV), wird in einem Dialog die Spannungsebene abgefragt.

⚠️An der Netznachbildung wird aktuell nicht gearbeitet, einige Funktionen können fehlerhaft sein.

#### Berechnung des Graphen: ####
Jedes Element des gezeichneten Netzes wird in einen Graphenknoten mit seinen Eigenschaften übertragen. Für jeden Transformator wird ein weiterer Knoten erstellt. 
  Ein Trafo wird also durch zwei Knoten repräsentiert, dies dient zum einen zur Darstellung von Anschlüssen an Ober-/Unterspannungsseite. Vor allem kann so aber der 
  Kante zwischen den beiden Knoten eine Impedanz zugewiesen werden, die in der Flussberechnung dann die unterschiedliche Kapazität von parallel geschalteten Trafos berücksichtigt und den Fluss dementsprechend realistisch berechnet.

Fragen und Anregungen gern an mich [per Mail](mailto:felix.husemann@tum.de)
~~~
Stand: 08.02.2023
© Felix Husemann, TUM
~~~