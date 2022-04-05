import { Component, OnInit, Input } from '@angular/core';
import { Location } from '@angular/common';
import { ActivatedRoute } from '@angular/router';

import { User } from '../user';
import { UserService } from '../user.service';

@Component({
  selector: 'app-user-edit',
  templateUrl: '../templates/user-edit.component.html'
})
export class UserEditComponent implements OnInit {
	
	@Input()
  user!: User;

	constructor(private route: ActivatedRoute, private userService: UserService, private location: Location) { }

	ngOnInit() {
		this.getUser();
	}
	
	getUser(): void {
		const id = + this.route.snapshot.paramMap.get('id')!;
		this.userService.getUser(id).subscribe(user => this.user = user);
	}
	
	save(): void {		
		this.userService.updateUser(this.user).subscribe(success=> {this.goBack();});
	}

	goBack(): void {
		this.location.back();
	}

}