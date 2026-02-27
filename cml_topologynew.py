name: Lab_5R_3S
nodes:
  # Routers
  - name: R1
    type: iosv
    x: 50
    y: 50
    interfaces:
      - name: GigabitEthernet0/0
        ip: 10.0.12.1/24
      - name: GigabitEthernet0/1
        ip: 10.0.15.1/24
  - name: R2
    type: iosv
    x: 150
    y: 50
    interfaces:
      - name: GigabitEthernet0/0
        ip: 10.0.12.2/24
      - name: GigabitEthernet0/1
        ip: 10.0.23.1/24
  - name: R3
    type: iosv
    x: 250
    y: 50
    interfaces:
      - name: GigabitEthernet0/0
        ip: 10.0.23.2/24
      - name: GigabitEthernet0/1
        ip: 10.0.35.1/24
  - name: R4
    type: iosv
    x: 350
    y: 50
    interfaces:
      - name: GigabitEthernet0/0
        ip: 10.0.34.2/24
      - name: GigabitEthernet0/1
        ip: 10.0.45.1/24
  - name: R5
    type: iosv
    x: 450
    y: 50
    interfaces:
      - name: GigabitEthernet0/0
        ip: 10.0.45.2/24
      - name: GigabitEthernet0/1
        ip: 10.0.15.2/24

  # Switches
  - name: S1
    type: iosvl2
    x: 50
    y: 150
    interfaces:
      - name: GigabitEthernet0/0
        ip: 10.0.15.3/24
  - name: S2
    type: iosvl2
    x: 250
    y: 150
    interfaces:
      - name: GigabitEthernet0/0
        ip: 10.0.35.3/24
  - name: S3
    type: iosvl2
    x: 450
    y: 150
    interfaces:
      - name: GigabitEthernet0/0
        ip: 10.0.15.4/24

links:
  # Router to Router
  - endpoints: [R1:GigabitEthernet0/0, R2:GigabitEthernet0/0]
  - endpoints: [R2:GigabitEthernet0/1, R3:GigabitEthernet0/0]
  - endpoints: [R3:GigabitEthernet0/1, R4:GigabitEthernet0/0]
  - endpoints: [R4:GigabitEthernet0/1, R5:GigabitEthernet0/0]

  # Routers to Switches
  - endpoints: [R1:GigabitEthernet0/1, S1:GigabitEthernet0/0]
  - endpoints: [R3:GigabitEthernet0/1, S2:GigabitEthernet0/0]
  - endpoints: [R5:GigabitEthernet0/1, S3:GigabitEthernet0/0]
