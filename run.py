from MessageBoard import create_app #imports from init.py file

app = create_app()

if __name__ == "__main__":
	app.run(debug=True)