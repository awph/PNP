PNP
===

PNP is a compiler that creates SVG files



objects :

	p1 = point : x(<int>) : y(<int>);
	l1 = line : p1(<point>) : p2(<point>) : color(blue) : width(<int>);
	c1 = circle : c(<point>) : r(<int>) : border-color(red) : border-width(<int>) : fill-color(blue);
	r1 = rect : o(<point>) : width(<int>) : height(<int>) : rx(<int>) : ry(<int>) : border-color(red) : border-width(<int>) : fill-color(blue);
	e1 = ellipse : c(<point>) : ry(<int>) : rx(<int>) : border-color(red) : border-width(<int>) : fill-color(blue);
	s1 = shape : p(<point>) : p(<point>) : p(<point>) : p(<point>) : ... : border-color(red) : border-width(<int>) : close(<bool>) : fill-color(blue);
	t1 = text : p(<point>) : font(<string>) : size(<int>) : color(black);


transformations :

	R1 = rotate : angle(<int>) : c(<point>);
	S1 = scale : sx(<int>) : sy(<int>);
	T1 = translate : p(<point>);


controls :

	if <condition>
	{
		<body>
	}

	while <condition>
	{
		<body>
	}

	for <int> : <int>
	{
		<body> // variable step = iteration en cours
	}
