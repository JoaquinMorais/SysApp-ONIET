drop database if EXIST Binance
create database Binance


create table usuarios(idUsuario int primary key,username varchar(50),password varchar(50));
create table registros(idRegistro int primary key,monto int,descripcion varchar(100),tipo varchar(1),fecha date,PlataTotal int,idUsuario int, constraint foreign key (idUsuario) references usuarios(idUsuario));
