PNP
===

PNP is a compiler that creates SVG files.

PNP language is defined
-

### Arithmetical operators ###
	+ : integer addition
	- : integer subtraction
	* : integer multiplication
	/ : integer division
	% : integer modulo
	= : affectation

### Logical operators ###
	< : lesser than
	> : greater than
	<= : lesser  or equals
	>= : greater or equals
	== : equals

### Primitive types ###
	int : integer
	string : characters
	boolean : YES or NO

### Shapes ###

	aColor = color : rgb(<int>, <int>, <int>) : hex(<string>) : name(<string>);
	aPoint = point : x(<int>) : y(<int>);
	aLine = line : p1(<point>) : p2(<point>) : fill_color(<color>) : width(<int>);
	aCircle = circle : c(<point>) : r(<int>) : border_color(<color>) : border_width(<int>) : fill_color(<color>);
	aRect = rect : o(<point>) : width(<int>) : height(<int>) : rx(<int>) : ry(<int>) : border_color(<color>) : border_width(<int>) : fill_color(<color>);
	anEllipse = ellipse : c(<point>) : ry(<int>) : rx(<int>) : border_color(<color>) : border_width(<int>) : fill_color(<color>);
	aCustomShape = customshape : p(<point>) : p(<point>) : p(<point>) : p(<point>) : ... : border_color(<color>) : border_width(<int>) : close(<bool>) : fill_color(<color>);
	aText = text : content(<string>) : p(<point>) : font(<string>) : size(<int>) : fill_color(<color>);


### Transformations ###

	aRotation = rotate : angle(<int>) : c(<point>);
	aScale = scale : sx(<int>) : sy(<int>);
	aTranslation = translate : p(<point>);
	displayOrHide = hide : h(<bool>);

### Controls ###

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


### Hello World! ###

	display = hide : h(NO);
	textPosition = point : x(20) : y(20);
	myHelloWorld = text : content("Hello world!") : p(textPosition);
	
	apply display
	{
		myHelloWorld;
	}
