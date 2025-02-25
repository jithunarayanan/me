# BBR (Bottleneck Bandwidth and Round-trip propagation time)

BBR (Bottleneck Bandwidth and Round-trip propagation time) is a TCP congestion control algorithm designed to optimize network performance, especially in high-speed environments. Enabling BBR can significantly enhance network efficiency. Here’s how to do it:

**Check Current TCP Congestion Control Algorithm:**

Before enabling BBR, determine the current TCP congestion control algorithm your system uses. Run this command in the terminal:

```
sysctl net.ipv4.tcp_congestion_control
```
The output will show the active algorithm (usually “cubic” by default).

**Enable BBR via CLI Commands:**
1. Edit the sysctl configuration file using this command:
```
sudo nano /etc/sysctl.conf
```
2. Add the following lines at the end of the file:

```
net.core.default_qdisc=fq
net.ipv4.tcp_congestion_control=bbr
```

Save and close the file.

3. Apply Changes:
Apply the new configuration using:
```
sudo sysctl -p
```
4. Verify BBR is Enabled:

Check if BBR is now the active algorithm:
```
sysctl net.ipv4.tcp_congestion_control
```
It should display “bbr” as the current setting.

**Use Cases for BBR:**

1. High-Speed Networks: BBR optimizes bandwidth utilization, making it ideal for high-speed networks.

1. Responsive Congestion Control: BBR adjusts transmission rates based on both bandwidth and round-trip time, ensuring efficient network utilization.

1. Efficient Data Transmission: BBR improves data transmission reliability, benefiting various network-dependent applications and services.

By enabling BBR, you’ll notice improved network stability and performance, especially in scenarios where efficient bandwidth usage matters. 🚀