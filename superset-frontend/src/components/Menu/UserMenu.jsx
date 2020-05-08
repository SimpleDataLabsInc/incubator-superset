/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
import React from 'react';
import PropTypes from 'prop-types';
import { NavDropdown, MenuItem } from 'react-bootstrap';
import { t } from '@superset-ui/translation';

const propTypes = {
  userInfoUrl: PropTypes.string.isRequired,
  userLogoutUrl: PropTypes.string.isRequired,
  versionString: PropTypes.string,
  versionSha: PropTypes.string,
};

export default function UserMenu({
  userInfoUrl,
  userLogoutUrl,
  versionString,
  versionSha,
}) {
  return (
      null
    /*<NavDropdown
      id="user-menu-dropwn"
      title={
        <>
          <i className="fa fa-user" />
        </>
      }
    >
      <MenuItem href={userInfoUrl}>
        <span className="fa fa-fw fa-user" />
        {t('Profile')}
      </MenuItem>
      <MenuItem href={userLogoutUrl}>
        <span className="fa fa-fw fa-sign-out" />
        {t('Logout')}
      </MenuItem>
      {(versionString || versionSha) && (
        <li className="version-info">
          {versionString && <div>Version: {versionString}</div>}
          {versionSha && <div>SHA: {versionSha}</div>}
        </li>
      )}
    </NavDropdown>*/
  );
}

UserMenu.propTypes = propTypes;
