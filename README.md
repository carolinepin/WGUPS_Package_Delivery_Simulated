# WGUPS_Package_Delivery_Simulated
Project originally from WGU to create a simulated automated UPS delivery process.
Purpose:
  Create a python based application that simulates picking up packages, deciding the closest package location, driving to it to drop off the package, time stamp pick up and drop off times, and repeat the process until all packages are delivered. The program ingests two CSV sheets, one that describes all the packages that need to be delivered, and the second one that lists the distances between the destination of all packages.

Things I want to work on:
- GUI to see progress of trucks/updates
- Multi-threading to allow for both trucks to run at the same time
- standardization of the "special notes" section of the package to allow for true automation as opposed to simulated human interpretation
- See if i can get the O(n) down from O(n^3). Not sure how/if I can do this, but it is at least worth looking into
