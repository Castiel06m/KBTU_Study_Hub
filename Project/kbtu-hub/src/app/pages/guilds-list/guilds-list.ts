import { Component, OnInit, ChangeDetectorRef} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Api } from '../../services/api';
import { Guild } from '../../models/course.model';

@Component({
  selector: 'app-guilds-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './guilds-list.html',
  styleUrls: ['./guilds-list.css']
})
export class GuildsList implements OnInit {
  guilds: Guild[] = [];
  selectedGuild: Guild | null = null;
  selectedFile: File | null = null;
  messages: any[] = [];
  newMessage: string = '';

  showCreateForm = false;
  newGuild = {
    name: '',
    description: ''
  };

  constructor(public api: Api, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.loadGuilds();
  }

  loadGuilds() {
    this.api.getGuilds().subscribe({
      next: (data) => {
        this.guilds = data;
        this.cdr.detectChanges();
      },
      error: (err) => console.error(err)
    });
  }

  selectGuild(guild: Guild) {
    this.selectedGuild = guild;
    this.loadMessages(guild.id);
  }

  loadMessages(guildId: number) {
    this.api.getMessages(guildId).subscribe(data => {
      this.messages = data;
      this.cdr.detectChanges();
    });
  }

  join(guildId: number) {
    this.api.joinGuild(guildId).subscribe({
      next: () => {
        alert('Успешно вступили!');
        this.loadGuilds(); 
      },
      error: (err) => alert('Ошибка или вы уже там')
    });
  }

  sendMsg(isUrgent: boolean = false) {
    if (!this.newMessage.trim() && !this.selectedFile) return; 
    if (!this.selectedGuild) return;
    this.api.sendMessage(
      this.selectedGuild.id, 
      this.newMessage, 
      isUrgent, 
      this.selectedFile 
    ).subscribe({
      next: () => {
        this.newMessage = '';
        this.selectedFile = null; 
    
        const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
        if (fileInput) fileInput.value = '';
      
        this.loadMessages(this.selectedGuild!.id);
        this.cdr.detectChanges();
      },
      error: (err) => alert('Ошибка при отправке')
    });
  }

  createGuild() {
    if (!this.newGuild.name.trim()) return;

    this.api.createGuild(this.newGuild).subscribe({
      next: () => {
        this.loadGuilds(); 
        this.newGuild = { name: '', description: '' }; 
        this.showCreateForm = false; 
        this.cdr.detectChanges();
      },
      error: (err) => alert('Ошибка при создании гильдии')
    });
  }

  replyToUrgent(msg: any) {
    if (msg.is_urgent) {
      this.newMessage = `@${msg.sender_username}, отвечаю на твой клич: `;
      document.querySelector('input')?.focus();
    }
  }

  onFileSelected(event: any) {
  const file: File = event.target.files[0];
  if (file) {
    this.selectedFile = file;
    }
  }
}