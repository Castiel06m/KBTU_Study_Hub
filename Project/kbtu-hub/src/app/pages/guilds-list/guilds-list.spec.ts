import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GuildsList } from './guilds-list';

describe('GuildsList', () => {
  let component: GuildsList;
  let fixture: ComponentFixture<GuildsList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GuildsList]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GuildsList);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
