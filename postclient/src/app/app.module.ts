import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { PostListComponent } from './post-list.component';
import { PostDetailComponent } from './post-detail.component';

@NgModule({
  declarations: [
    AppComponent,
    PostListComponent,
    PostDetailComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
