const fs = require('fs');

const names = [
  'Simon',
  'Milo',
  'Garry',
  'Tristan',
  'Nick',
  'Ed',
  'Calum',
  'Matt',
  'Jack',
  'Ana',
  'Tatiana',
  'Dani',
];

const superUser = {
  model: 'jwt_auth_app.holiuser',
  pk: names.length,
  fields: {
    username: 'marco',
    email: 'marco@gmail.com',
    password: 'password',
    is_superuser: true,
    is_staff: true,
    image: 'xxx',
    bio: 'x',
  },
};

const users = [
  ...names.map((name, idx) => ({
    model: 'jwt_auth_app.holiuser',
    pk: idx + 1,
    fields: {
      username: name,
      email: `${name.toLowerCase()}@gmail.com`,
      password: 'password',
      image: '',
      bio: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Placeat tempora necessitatibus ducimus impedit aliquid maxime odit nostrum. Voluptate delectus inventore magnam. Consectetur, velit. Consequuntur nemo excepturi distinctio maiores vero minima!',
    },
  })),
  superUser,
];

fs.writeFileSync('./fixture.json', JSON.stringify(users));
