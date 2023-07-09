const express = require('express');
const exphbs = require('express-handlebars');
const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');
const bodyParser = require('body-parser')

const app = express();

/*****************************************
 * Engine
 *****************************************/
app.engine('hbs', exphbs.engine({
    defaultLayout: 'main',
    extname: '.hbs'
}));

app.set('view engine', 'hbs');


/*****************************************
 * DB
 *****************************************/
const dbFile = 'db.sqlite';
if (!fs.existsSync(dbFile)) {
    let db = new sqlite3.Database(dbFile);
    db.serialize(function() {
        db.run(`create table users (
                id INTEGER PRIMARY KEY, 
                first_name varchar(255), 
                last_name varchar(255), 
                email varchar(255) UNIQUE, 
                password varchar(255)
            )`
        )
    })
}

app.use(bodyParser.urlencoded({extended: true}))
app.use(express.static('public'))


/*****************************************
 * Routes
 *****************************************/
app.get('/', (req, res) =>  {
    res.render('index!')
})

app.get('/signup', (req,res) => {
    res.render('signup', {title: 'Join!'})
})

app.post('/signup', (req,res) => {
    const { first_name, last_name, email, password } = req.body;

    const db = new sqlite3.Database('db.sqlite');
    const sql = `INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)`;

    db.run(sql, [first_name, last_name, email, password], function(err) {
        if (err) {
        console.error(err.message);
        return res.status(500).send('Error creating user');
        }
        
        console.log(`User with email ${email} created successfully`);
        return res.status(200).send('User created successfully');
    });

    db.close();
})


app.listen(3000, () => {
    console.log('Example app listening on port 3000!')
})


