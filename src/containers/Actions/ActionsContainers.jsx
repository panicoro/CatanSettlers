import React from 'react';

/* eslint-disable import/no-named-as-default */
import ActionButton from './ActionButton';
import BankTrade from './BankTrade';
import Robbing from './Robbing';
import BuildingVertex from './BuildingVertex';
import BuildingEdge from './BuildingEdge';
import Roads from './Roads';
import Jumbotron from 'react-bootstrap/Jumbotron';
/* eslint-enable import/no-named-as-default */

import '../../components/General.css'

const actionsContainers = {
  moveRobber: <Jumbotron id='jumbo_robber'>
                <ActionButton type="move_robber" />
              </Jumbotron>,
  buying: <BankTrade />,
  knightRobbing: <Robbing type="play_knight_card" />,
  robberRobbing: <Robbing type="move_robber" />,
  buildingCity: <BuildingVertex type="upgrade_city" />,
  buildingRoad: <BuildingEdge />,
  buildingSettlement: <BuildingVertex type="build_settlement" />,
  roads: <Roads />,
};

export default actionsContainers;
