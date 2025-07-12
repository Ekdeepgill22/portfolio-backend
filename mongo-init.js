// MongoDB initialization script
db = db.getSiblingDB('portfolio_db');

// Create a user for the portfolio database
db.createUser({
  user: 'portfolio_user',
  pwd: 'portfolio_password',
  roles: [
    {
      role: 'readWrite',
      db: 'portfolio_db'
    }
  ]
});

// Create the contacts collection with validation
db.createCollection('contacts', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['name', 'email', 'subject', 'message', 'created_at'],
      properties: {
        name: {
          bsonType: 'string',
          description: 'must be a string and is required'
        },
        email: {
          bsonType: 'string',
          pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$',
          description: 'must be a valid email and is required'
        },
        subject: {
          bsonType: 'string',
          description: 'must be a string and is required'
        },
        message: {
          bsonType: 'string',
          description: 'must be a string and is required'
        },
        created_at: {
          bsonType: 'date',
          description: 'must be a date and is required'
        },
        ip_address: {
          bsonType: 'string',
          description: 'must be a string'
        },
        user_agent: {
          bsonType: 'string',
          description: 'must be a string'
        }
      }
    }
  }
});

// Create indexes for better performance
db.contacts.createIndex({ email: 1 });
db.contacts.createIndex({ created_at: -1 });
db.contacts.createIndex({ name: 1, email: 1 });

print('Database initialization completed successfully!');