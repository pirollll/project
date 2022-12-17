INSERT INTO msgs (sender, message) VALUES ("Evandro", "Primeira mensagem aqui!");


INSERT INTO msgs (sender, message) VALUES ("Joao", "Consegui a primeira mensagem sera?!");


INSERT INTO users (username, hash) VALUES ("novo", "pbkdf2:sha256:260000$c8c8J0ndSocG39lQ$5b5c973a4c7157b7933899f19167016d55fa052078fb38a2dd045e6d0094fd2e");


SELECT * FROM msgs ORDER BY created_at DESC LIMIT 1;


DELETE FROM msgs;


SELECT EXISTS (SELECT 1 FROM msgs);


SELECT msgs.created_at, message, sender, avatar FROM msgs INNER JOIN users on msgs.sender = users.username ORDER BY created_at DESC LIMIT 1


SELECT created_at, message, sender, avatar 
    FROM msgs INNER JOIN users 
    ON msgs.sender = users.username OR msgs.sender LIKE "Guest%"
    GROUP BY created_at ORDER BY created_at;


SELECT avatar 
FROM users


SELECT created_at, message, sender 
FROM msgs;