import { Expose, classToPlain, plainToClass, plainToInstance } from "class-transformer";

class User {
  @Expose() id: number;
  @Expose() name: string;
  @Expose() email: string;
  @Expose() addresses: Address[];

  constructor(id: number, name: string, email: string, addresses: Address[]) {
    this.id = id;
    this.name = name;
    this.email = email;
    this.addresses = addresses;
  }
}
  
class Address {
  street: string;
  city: string;
  country: string;

  constructor(street: string, city: string, country: string) {
    this.street = street;
    this.city = city;
    this.country = country;
  }
}

var user = new User(1,'sdf','sdf', [new Address('sdf','fds','ert')])
// console.log(JSON.stringify(user))
//{"id":1,"name":"sdf","email":"sdf","addresses":[{"street":"sdf","city":"fds","country":"ert"}]}

var x = plainToInstance(User, '{"id":1,"name":"sdf","email":"sdf","addresses":[{"street":"sdf","city":"fds","country":"ert"}]}', { excludeExtraneousValues: true })
console.log(typeof x)





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
  