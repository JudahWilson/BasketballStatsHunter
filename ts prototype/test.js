"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var class_transformer_1 = require("class-transformer");
var User = /** @class */ (function () {
    function User(id, name, email, addresses) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.addresses = addresses;
    }
    return User;
}());
var Address = /** @class */ (function () {
    function Address(street, city, country) {
        this.street = street;
        this.city = city;
        this.country = country;
    }
    return Address;
}());
var user = new User(1, 'sdf', 'sdf', [new Address('sdf', 'fds', 'ert')]);
// console.log(JSON.stringify(user))
//{"id":1,"name":"sdf","email":"sdf","addresses":[{"street":"sdf","city":"fds","country":"ert"}]}
var x = (0, class_transformer_1.plainToInstance)(User, '{"id":1,"name":"sdf","email":"sdf","addresses":[{"street":"sdf","city":"fds","countr":"ert"}]}', { excludeExtraneousValues: true });
console.log(typeof x);
// {
//   "id": 1,
//   "name": "John Doe",
//   "email": "john@example.com",
//   "addresses": [
//     {
//       "street": "123 Main St",
//       "city": "New York",
//       "country": "USA"
//     },
//     {
//       "street": "456 Elm St",
//       "city": "Los Angeles",
//       "country": "USA"
//     }
//   ]
// }
