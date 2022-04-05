import { Component, OnInit } from '@angular/core';

import { ActivatedRoute } from '@angular/router';
import { User } from '../user';
import { UserService } from '../user.service';

@Component({
  selector: 'app-user-list',
  templateUrl: '../templates/user-list.component.html'
})
export class UserListComponent implements OnInit {

	users: any = [];

	constructor(private route: ActivatedRoute, private userService: UserService) { }

	ngOnInit() {
		this.getUsers();
	}

	getUsers(): void {
		this.userService.getUsers().subscribe(users => {
			this.users = users;

			for (let i = 0; i < this.users.length; i++ ){
				let object: User = {
					id: this.users[i][0],
					name: this.users[i][1],
					email: this.users[i][2],
					pwd: this.users[i][3]
				}; 
				this.users[i] = object;
			};

		});
	}
  
	delete(user: User): void {
		this.userService.deleteUser(user).subscribe(success=> {this.getUsers();});		
	}

}