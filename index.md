

<html>
  <head>
    <title>Ion</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

  </head>
  <body>
      <div class="header">
        <h1>Open Probability of Ion Channels </h1>
        <p>Adam Berridge, Phil Vorce, Irene Galca, Jordan Hiatt</p>
      </div>


      <div class="abstract">
        <h2>Abstract</h2>
        <p>
          Our sponsor's research consists of collecting data on the amount of current
          across a membrane in response to an increase in voltage. As voltage increases
          the current rises linearly for some time before tapering off due to ion
          channels closing. Our sponsor requested a software tool to analyze these
          data points and the data points of a linear regression representing projected
          values had all ion channels remained opened. He also requested a way to
          visualize the actual current over the projected current if all ion channels
          remained open, commonly referred to as the open probability of the membrane.
        </p>
      </div>


      <div class="description">
        <h2>Project Description</h2>
        <p>
          Our solution was build a graphical user interface using the Python programming
          language. A .csv file can be seleccted from disk. If the data in the file
          is properly formatted two graphs are plotted. The first graph holds the data from the
          .csv, along with an interactive regression line. The second graph charts
          the open probability. The values of the regression and open probability can
          be saved to disk.
        </p>
      </div>


      <img src="openProb.png" style="width:auto; height:500px; display:block; margin-left:auto; margin-right:auto;">
     </body>
</html>
