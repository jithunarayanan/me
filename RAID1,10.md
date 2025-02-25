# Raid 0+1 vs Raid 1+0 (Probability of Failure)

Here's a little bit of math that should show the differences in rates of failure. For simplicity, let's assume there is an even number of disks.

In both array configurations, each disk is broken up into blocks. In Raid 0+1, striping occurs first and then mirroring. In Raid 1+0, mirroring 
occurs first and then striping.

We can always partition Raid 0+1 into two groups (G1 and G2).
Note that I'm using 'partition' in a mathematical sense.
~~~
For n disks, we can define:
G1 = {D1, D2, ..., Dn/2}
G2 = {Dn/2+1, Dn/2+2, ..., Dn}
~~~
**Raid 0+1**
~~~
4 Disks:                       6 Disks:
Disk1 Disk2 Disk3 Disk4        Disk1 Disk2 Disk3 Disk4 Disk5 Disk6
----- ----- ----- -----        ----- ----- ----- ----- ----- -----
| a | | b | | a | | b |        | a | | b | | c | | a | | b | | c |
| c | | d | | c | | d |        | d | | e | | f | | d | | e | | f |
----- ----- ----- -----        ----- ----- ----- ----- ----- -----
G1 = {D1, D2}                  G1 = {D1, D2, D3}
G2 = {D3, D4}                  G2 = {D4, D5, D6}
~~~

For Raid 1+0, we can always partition the disks into n/2 groups.
Note that I'm using 'partition' in a mathematical sense.
For n disks, we can define:
G1 = {D1, D2}
G2 = {D3, D4}
...
Gn/2 = {Dn-1, Dn}

**Raid 1+0**

~~~
4 Disks:                       6 Disks:
Disk1 Disk2 Disk3 Disk4        Disk1 Disk2 Disk3 Disk4 Disk5 Disk6
----- ----- ----- -----        ----- ----- ----- ----- ----- -----
| a | | a | | b | | b |        | a | | a | | b | | b | | c | | c |
| c | | c | | d | | d |        | d | | d | | e | | e | | f | | f |
----- ----- ----- -----        ----- ----- ----- ----- ----- -----
G1 = {D1, D2}                  G1 = {D1, D2}
G2 = {D3, D4}                  G2 = {D3, D4}
                               G3 = {D5, D6}
~~~
Now, with that out of the way, let's get into some math!
For a failure to occur in a Raid 0+1 configuration, at least 1 hard disk from each group must die.
For a failure to occur in a Raid 1+0 configuration, all hard disks in any single group must die.

In either Raid configuration, at least two disks must die. Let's look at all the possible ways both Raid configurations could fail if two disks were to die.


      Number of Disks (n) = 4
      2 Disks Die : Raid Failure
      D1D2        : R10
      D1D3        : R01
      D1D4        : R01
      D2D3        : R01
      D2D4        : R01
      D3D4        : R10

With 4 disks, there are C(n, 2) = C(4, 2) = 6 combinations in total.

4/6 of these combinations would cause a Raid 0+1 configuration to fail. (66% chance of failure)

We can say that:

      P1 = P (Raid 0+1 Failure | 2 Disks die) = 2/3

2/6 of these combinations would cause a Raid 1+0 configuration to fail. (33% chance of failure)

We can say that:

      P2 = P (Raid 1+0 Failure | 2 Disks die) = 1/3

We can do the same test with n = 6, but I'll omit the table.

      P1 = 9/15 = 3/5
      P2 = 3/15 = 1/5
      P3 = P (No failures | 2 Disks die) = 4/15
      P1P2 = 1/15

With 6 disks, there are c(n, 2) = c(6, 2) = 15 possible combinations.

There is a 60% chance that a Raid 0+1 configuration fails.
There is a 20% chance that a Raid 1+0 configuration fails.

Now these results can be generalized for n disks.
~~~
P1 = c(n/2, 1) * c(n/2, 1) / c(n, 2)
   = (n/2 * n/2) / (n * (n - 1) / 2)
   = (n/2 * n/2) * (2 / (n * (n - 1))
   = (n * n / 4) * (2 / (n * (n - 1))
   = (n / 2) * (1 / (n - 1))
   = n / (2 * (n - 1))
~~~
~~~
P2 = (n/2) / c(n, 2)
   = (n/2) / (n * (n - 1) / 2)
   = (n/2) * (2 / (n * (n - 1)))
   = 1 / (n - 1)
~~~

Now the most useful and interesting part of the math. We can take the limits of the two equations above. Below, I use 'inf' to mean infinity.

Lim n->inf P1 = Lim n->inf n / (2 * (n - 1))     // We can use L'Hopital's rule

    = Lim n->inf 1 / 2 = 1 / 2
In other words, there will always be at least a 50% chance of failure if 2 disks die on a Raid 0+1 configuration!


Now let's see how a Raid 1+0 configuration fairs.

Lim n->inf P2 = Lim n->inf 1 / (n - 1) = 0
In other words, the more disks we add to a raid 1+0 configuration, the closer to a theoretical 0% chance of failure we get!


One final table (Please note that I am rounding the values to integers.)

    -------------------
    | n   | P1  | P2  |
    -------------------
    | 4   | 66% | 33% |
    | 6   | 60% | 20% |
    | 8   | 57% | 14% |
    | 10  | 55% | 11% |
    | 12  | 54% | 9%  |
    | 16  | 53% | 7%  |
    | 20  | 52% | 5%  |
    | 24  | 52% | 4%  |
    | 32  | 51% | 3%  |
    | 64  | 50% | 1%  |
    | 128 | 50% | 0%  |
    -------------------

**Conclusion:**
<br>Use Raid 1+0.
