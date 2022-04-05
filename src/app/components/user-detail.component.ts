import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';
import { ActivatedRoute } from '@angular/router';

import { User } from '../user';
import { UserService } from '../user.service';

@Component({
  selector: 'app-user-detail',
  templateUrl: '../templates/user-detail.component.html'
})
export class UserDetailComponent implements OnInit {
	user!: User;
	
	constructor(private route: ActivatedRoute, private userService: UserService, private location: Location) { }
	
	ngOnInit() {
		this.getUser();
	}
	
	getUser(): void {
		const id = + this.route.snapshot.paramMap.get('id')!;
		this.userService.getUser(id).subscribe(user => {
			let obj: any = user;
			this.user = {
				id: obj[0],
				name: obj[1],
				email: obj[2],
				pwd: obj[3]
			};
		});
	}

	goBack(): void {
		this.location.back();
	}

}