SET foreign_key_checks = 0;
drop table if exists HouseRoof;
create table HouseRoof (
	id int primary key,
	subtitle text,
	result text
);

drop table if exists HouseDoor;
create table HouseDoor (
	id int primary key,
	subtitle text,
	result text
);

drop table if exists HouseWindow;
create table HouseWindow (
	id int primary key,
	subtitle text,
	result text
);

/*지붕 유무, 크기 모델*/
insert into HouseRoof(id, subtitle, result)
values(0, "지붕을 그리지 않은 경우 (높낮이 없는 일자 지붕도 포함)",
"- 지붕이 없거나 높낮이가 없는 일자 지붕을 그린 당신은 공상력이 없는 사람으로 보입니다. 위축된 성격을 갖고 구체적인 것만을 추구하는 사람들에게서 나타나는 편입니다. 만약 지붕을 아예 그리지 않았다면, 가정 구조와 개념이 불명확하게 잡혀있다고 해석될 수 있습니다.")

insert into HouseRoof(id, subtitle, result)
values(1, "지붕의 크기가 큰 경우",
"- 큰 지붕을 그린 당신은 환상을 꿈꾸고 상상령이 풍부한 편입니다. 공상을 좋아하고, 현실과 인간관계를 도피하려는 경향이 있습니다. 지붕은 특히 공상영역을 상징하므로, 지나치게 큰 지붕은 공상에 열중하며 외면적인 대인관계로부터 도피하려는 경향을 나타내기도 합니다.")

/*문 유무, 크기 모델*/
insert into HouseDoor(id, subtitle, result)
values(0, "문을 그리지 않은 경우",
"- 문을 그리지 않은 당신은 외부세계에 방어적인 심리가 강하고 타인과 자신의 교류를 거부하고 있습니다. 당신은 냉담, 위축, 괴리되는 느낌이 있는 사람일 수 있습니다. 숨기려는 성향이 강하여, 폐쇠적이고 가정내부에 사적인 비밀이 있을 수 있습니다. 특히, 가족 구성원들과 정신적 교류가 결여되고 끈끈한 정이 부족한 상황에 놓여있을 수 있습니다.")

insert into HouseDoor(id, subtitle, result)
values(1, "문을 크게 그린 경우",
"- 문의 크기가 큰 경우, 당신은 수줍음이 많고 인간관계가 부족한 가능성이 있는 것으로 해석됩니다. 따라서, 신중하고 수동적인 성향입니다. 만일 문이 매우 크고 웅장하다면, 타인에게 과도하게 의존하는 경향이 있을 수 있습니다. 당신은 적극적으로 사회와의 접촉을 갈망하고 있으며, 다른 사람에게 이해받고 싶어 하는 마음이 큰 상태로 보입니다.")

insert into HouseDoor(id, subtitle, result)
values(2, "문을 작게 그린 경우",
"- 문의 크기가 작은 경우, 겉으로는 개방적이나 내적으로는 타인의 접근을 거부하고 있는 것처럼 보입니다. 환경과의 접촉을 꺼려하고, 무력감을 느끼고 있을 가능성이 있습니다. 만일 들어갈 수 없을 정도로 작은 문을 그렸다면, 타인과 소통하고자하는 강한 바람이 없다는 의미입니다. 당신은 사교를 회피하고 무기력한 상태에 놓여있을 수 있습니다.")

/*창 개수, 크기 모델*/
insert into HouseWindow(id, subtitle, result)
values(0, "창을 그리지 않은 경우",
"- 창이 없는 그림을 그린 사람은 편집성향을 보이는 것으로 해석됩니다. 또한, 환경에 대한 관심이 결여되어 있고, 적의가 있거나 폐쇄적인 상태일 수 있습니다. 혹은 피해망상증이 있기도 합니다. 당신은 뒤로 물러서는 경우가 많고 위축되어 있는 일이 많아 보입니다. 만약, 창문도 없고 문도 없다면 정신분열증의 증후일 수 있습니다.")

insert into HouseWindow(id, subtitle, result)
values(1, "창을 여러 개 그린 경우 (2개 이상)",
"- 창의 개수는 외부세계에 대한 호기심과 욕구를 나타냅니다. 많은 창을 그린 사람은 개방적이고 사교적입니다. 또한, 타인의 교류를 간절히 원하며 외부환경과의 접촉을 많이 하고 싶은 사람일 가능성이 높습니다. ")

insert into HouseWindow(id, subtitle, result)
values(2, "큰(통유리창)을 그린 경우",
"- 창을 매우 크게 그린 당신은 개방적이고, 타인과의 소통을 원하고 있습니다. 또한, 타인에게 자신을 이해시키려 하는 경향이 있습니다.")

insert into EntireTree(id, subtitle, result)
values(3, "작은(좁은) 창을 그린 경우",
"- 창을 좁게 그린 당신은 소심하고 수줍음이 많은 사람으로 해석됩니다. 당신은 타인이 다가오지 못하게 하는 경우가 많습니다. 만일 창이 매우 작다면, 심리적으로 가까이 다가가기 어려운 사람일 가능성이 높습니다.")

select * from HouseRoof;
select * from HouseDoor;
select * from HouseWindow;