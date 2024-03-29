# Sonar-based obstacle-avoiding line follower

<img src="../img/example-sonar.jpg" width="400"/>

* **Wiring**

  Starting from the [line-follower](line_follower.md) wiring, plug in the RCWL-1601 sonar and connect its VCC and GND pin appropriately using two extra wires (S4, S7) as follows:

  ![](../img/example-sonar-wiring.jpg)

* **Programming**

  Change `code.py` to be just `import ex03_line_follower_sonar`.

* **Result**
  
  <iframe width="640" height="390" frameborder="0" allowfullscreen
          src="https://www.youtube.com/embed/cBlWqL9eYWU">
  </iframe>

  Note that you can hear the normally inaudible sonar working in the recording.
