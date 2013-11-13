PNP
===

PNP is a compiler that creates SVG files



objects :

	c0 = color : rgb(<int>, <int>, <int>) : hex(<string>) : name(<string>);
	p1 = point : x(<int>) : y(<int>);
	l1 = line : p1(<point>) : p2(<point>) : color(<color>) : width(<int>);
	c1 = circle : c(<point>) : r(<int>) : border-color(<color>) : border-width(<int>) : fill-color(<color>);
	r1 = rect : o(<point>) : width(<int>) : height(<int>) : rx(<int>) : ry(<int>) : border-color(<color>) : border-width(<int>) : fill-color(<color>);
	e1 = ellipse : c(<point>) : ry(<int>) : rx(<int>) : border-color(<color>) : border-width(<int>) : fill-color(<color>);
	s1 = shape : p(<point>) : p(<point>) : p(<point>) : p(<point>) : ... : border-color(<color>) : border-width(<int>) : close(<bool>) : fill-color(<color>);
	t1 = text : content(<string>) : p(<point>) : font(<string>) : size(<int>) : color(<color>);


transformations :

	R1 = rotate : angle(<int>) : c(<point>);
	S1 = scale : sx(<int>) : sy(<int>);
	T1 = translate : p(<point>);
	H1 = hide : h(<bool>);

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
	
	apply <transformations>
	{
		<object>;
		<object>;
	}
