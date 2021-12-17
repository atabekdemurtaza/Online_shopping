import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { PostListComponent } from './post-list.component';
import { PostDetailComponent } from './post-detail.component';
import { PostService } from './post.service';
import { FormModule } from '@angular/forms';
import { HttpClienModule } from '@angular/common/http';
import { registerLocaleDate } from '@angular/common';
import localeRu from '@angular/common/locales/ru';
import localeRuExtra from '@angular/common/locales/extra/ru';
import { LOCALE_ID } from '@angular/core';
import { Routes } from '@angular/router';

const appRoutes: Routes = [
  {path: ':pk', component: PostDetailComponent},
  {path: '', component: PostListComponent}
];

registerLocaleDate(localeRu, 'ru', localeRuExtra)


@NgModule({
  declarations: [
    AppComponent,
    PostListComponent,
    PostDetailComponent
  ],
  imports: [
    BrowserModule,
    HttpClienModule,
    FormModule
  ],
  providers: [
    PostService,
    {provide: LOCALE_ID, useValue: 'ru'}
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
